"""SEO-генератор статей через YandexGPT.

Улучшенная версия скрипта:
- валидация входного YAML + детальные ошибки;
- отложенная проверка переменных окружения (не при импорте, а при запуске);
- устойчивые HTTP-вызовы с retry/backoff;
- кэширование лемматизации для ускорения;
- безопасная точечная доправка фрагментов;
- CLI-параметры для удобного запуска.
"""

from __future__ import annotations

import argparse
import os
import random
import re
import time
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import pymorphy3
import requests
import yaml

API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
_FINAL_STATUSES = {"ALTERNATIVE_STATUS_FINAL", "ALTERNATIVE_STATUS_UNSPECIFIED"}
_TOKEN_RE = re.compile(r"[А-Яа-яЁёA-Za-z0-9]+(?:-[А-Яа-яЁёA-Za-z0-9]+)*")
_SCHEMA_RULES: list[tuple[str, type, bool]] = [
    ("task.topic", str, True),
    ("task.tone", str, True),
    ("output.structure", list, True),
    ("output.length_chars", int, False),
    ("keywords.must_use", list, True),
]


@dataclass(frozen=True)
class AppConfig:
    api_key: str
    folder_id: str
    model_name: str = "yandexgpt/latest"
    timeout_s: int = 60

    @property
    def model_uri(self) -> str:
        return f"gpt://{self.folder_id}/{self.model_name}"


def load_config_from_env() -> AppConfig:
    api_key = os.getenv("YANDEX_API_KEY", "").strip()
    folder_id = os.getenv("YANDEX_FOLDER_ID", "").strip()
    model_name = os.getenv("YANDEX_MODEL_NAME", "yandexgpt/latest").strip()

    missing = []
    if not api_key:
        missing.append("YANDEX_API_KEY")
    if not folder_id:
        missing.append("YANDEX_FOLDER_ID")

    if missing:
        raise EnvironmentError(
            "Не заданы обязательные переменные окружения: "
            f"{', '.join(missing)}. "
            "Пример: export YANDEX_API_KEY=... && export YANDEX_FOLDER_ID=..."
        )

    return AppConfig(api_key=api_key, folder_id=folder_id, model_name=model_name)


def _get_nested(dct: dict[str, Any], path: str) -> tuple[Any, bool]:
    node: Any = dct
    for key in path.split("."):
        if not isinstance(node, dict) or key not in node:
            return None, False
        node = node[key]
    return node, True


def validate_brief_schema(brief: dict[str, Any]) -> None:
    errors: list[str] = []

    if not isinstance(brief, dict):
        raise ValueError("brief.yaml должен содержать YAML-словарь (mapping) в корне.")

    for field_path, expected_type, must_be_nonempty in _SCHEMA_RULES:
        value, found = _get_nested(brief, field_path)
        if not found:
            errors.append(f"  - «{field_path}» отсутствует")
            continue

        if not isinstance(value, expected_type):
            errors.append(
                f"  - «{field_path}» должен быть {expected_type.__name__}, "
                f"а не {type(value).__name__} (текущее значение: {value!r})"
            )
            continue

        if must_be_nonempty and not value:
            errors.append(f"  - «{field_path}» не должен быть пустым")

    if errors:
        raise ValueError(
            "Бриф содержит ошибки схемы:\n"
            + "\n".join(errors)
            + "\nПроверьте brief.yaml и исправьте указанные поля."
        )


def load_brief(yaml_path: str) -> dict[str, Any]:
    with open(yaml_path, "r", encoding="utf-8") as file:
        brief = yaml.safe_load(file)
    validate_brief_schema(brief)
    print(f"✓ Бриф загружен и проверен: тема «{brief['task']['topic']}»")
    return brief


def build_prompt(brief: dict[str, Any]) -> tuple[str, str]:
    kw = brief["keywords"]
    must_use = kw["must_use"]
    should_use = kw.get("should_use", [])
    lsi = brief.get("lsi", {}).get("phrases", [])
    structure = brief["output"]["structure"]
    length = brief["output"]["length_chars"]
    constraints = brief.get("constraints", {})
    avoid = constraints.get("avoid", [])

    should_total = constraints.get("should_use_total", 5) if should_use else 0
    tone = brief["task"]["tone"]

    system = (
        f"Ты опытный SEO-копирайтер. Пишешь на русском языке. Тон: {tone}. "
        + (f"Никогда не используй: {', '.join(avoid)}. " if avoid else "")
        + "Строго соблюдай структуру и ключевые слова из задания."
    )

    user = f"""Напиши SEO-статью на тему: «{brief['task']['topic']}»

ОБЯЗАТЕЛЬНЫЕ ключевые слова (использовать каждое минимум 1 раз, точной или падежной формой):
{chr(10).join(f'  - {k}' for k in must_use)}
""" + (
        f"""
ЖЕЛАТЕЛЬНЫЕ ключевые слова (использовать суммарно не менее {should_total} раз):
{chr(10).join(f'  - {k}' for k in should_use)}
"""
        if should_use
        else ""
    ) + (
        f"""
LSI-фразы (использовать естественно, не перечислять подряд):
{chr(10).join(f'  - {p}' for p in lsi)}
"""
        if lsi
        else ""
    ) + f"""
СТРУКТУРА (соблюдать строго):
{chr(10).join(f'  {i + 1}. {s}' for i, s in enumerate(structure))}

Объём: около {length} символов.
Формат ответа: Markdown."""

    return system, user


def call_yandexgpt(
    config: AppConfig,
    system: str,
    user: str,
    *,
    temperature: float = 0.4,
    max_retries: int = 3,
) -> str:
    headers = {
        "Authorization": f"Api-Key {config.api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "modelUri": config.model_uri,
        "completionOptions": {
            "stream": False,
            "temperature": float(temperature),
            "maxTokens": "4000",
        },
        "messages": [
            {"role": "system", "text": system},
            {"role": "user", "text": user},
        ],
    }

    last_error: str | None = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(API_URL, headers=headers, json=body, timeout=config.timeout_s)
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = (2**attempt) + random.uniform(0, 0.5)
                print(
                    f"⚠ Попытка {attempt}/{max_retries}: статус {resp.status_code}, "
                    f"повтор через {wait:.1f}с..."
                )
                time.sleep(wait)
                last_error = f"HTTP {resp.status_code}"
                continue

            resp.raise_for_status()
            try:
                data = resp.json()
            except ValueError as exc:
                raise RuntimeError(
                    f"API вернул не-JSON ответ: {resp.text[:800]}"
                ) from exc

            payload = data.get("result", data)
            alternatives = payload.get("alternatives") or []
            if not alternatives:
                raise RuntimeError(f"Пустой список alternatives. Ответ API:\n{data}")

            alt = alternatives[0]
            status = alt.get("status", "ALTERNATIVE_STATUS_UNSPECIFIED")
            if status not in _FINAL_STATUSES:
                raise RuntimeError(
                    f"Модель вернула нефинальный статус: {status}.\n"
                    f"Полный ответ: {data}"
                )

            text = alt.get("message", {}).get("text", "").strip()
            if not text:
                raise RuntimeError(f"В ответе нет текста. Ответ API:\n{data}")

            print(f"✓ Модель ответила ({len(text)} символов)")
            return text

        except requests.RequestException as exc:
            wait = (2**attempt) + random.uniform(0, 0.5)
            print(
                f"⚠ Попытка {attempt}/{max_retries}: сетевая ошибка ({exc}), "
                f"повтор через {wait:.1f}с..."
            )
            time.sleep(wait)
            last_error = str(exc)

    raise RuntimeError(f"Все {max_retries} попытки исчерпаны. Последняя ошибка: {last_error}")


_morph = pymorphy3.MorphAnalyzer()


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


@lru_cache(maxsize=50_000)
def _lemma(token: str) -> str:
    parsed = _morph.parse(token)
    return parsed[0].normal_form if parsed else token


def _lemmatize_tokens(tokens: list[str]) -> list[str]:
    return [_lemma(token) for token in tokens]


def _normalize_phrase(phrase: str) -> str:
    return " ".join(phrase.lower().split())


def _phrase_in_text_normalized(phrase: str, text: str) -> bool:
    return _normalize_phrase(phrase) in _normalize_phrase(text)


def _phrase_in_text_lemmatized(phrase: str, text_lemmas: list[str], max_gap: int = 2) -> bool:
    kw_lemmas = _lemmatize_tokens(_tokenize(phrase))
    if not kw_lemmas:
        return False

    start_positions = [i for i, lemma in enumerate(text_lemmas) if lemma == kw_lemmas[0]]
    for start in start_positions:
        pos = start
        matched = 1
        for kw_lemma in kw_lemmas[1:]:
            window = text_lemmas[pos + 1 : pos + 1 + max_gap + 1]
            if kw_lemma in window:
                pos = pos + 1 + window.index(kw_lemma)
                matched += 1
            else:
                break
        if matched == len(kw_lemmas):
            return True

    return False


def _count_phrase_occurrences(phrase: str, text_lemmas: list[str], max_gap: int = 2) -> int:
    kw_lemmas = _lemmatize_tokens(_tokenize(phrase))
    if not kw_lemmas:
        return 0

    count = 0
    i = 0
    while i < len(text_lemmas):
        if text_lemmas[i] == kw_lemmas[0]:
            pos = i
            matched = 1
            for kw_lemma in kw_lemmas[1:]:
                window = text_lemmas[pos + 1 : pos + 1 + max_gap + 1]
                if kw_lemma in window:
                    pos = pos + 1 + window.index(kw_lemma)
                    matched += 1
                else:
                    break

            if matched == len(kw_lemmas):
                count += 1
                i = pos + 1
                continue

        i += 1

    return count


def validate_keywords(text: str, must_use: list[str]) -> tuple[list[str], list[str]]:
    text_lemmas = _lemmatize_tokens(_tokenize(text))
    found: list[str] = []
    missing: list[str] = []

    for keyword in must_use:
        if _phrase_in_text_normalized(keyword, text) or _phrase_in_text_lemmatized(keyword, text_lemmas):
            found.append(keyword)
        else:
            missing.append(keyword)

    return found, missing


def count_should_use(text: str, should_use: list[str]) -> int:
    if not should_use:
        return 0
    text_lemmas = _lemmatize_tokens(_tokenize(text))
    return sum(_count_phrase_occurrences(phrase, text_lemmas) for phrase in should_use)


def _find_relevant_paragraphs(
    text: str, missing_keywords: list[str], max_paragraphs: int = 3
) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    kw_words: set[str] = set()
    for kw in missing_keywords:
        kw_words.update(_tokenize(kw))

    relevant: list[str] = []
    for para in paragraphs:
        para_words = set(_tokenize(para))
        if kw_words & para_words:
            relevant.append(para)
        if len(relevant) >= max_paragraphs:
            break

    if not relevant and paragraphs:
        relevant = [paragraphs[-1]]

    return relevant


def patch_missing_keywords(config: AppConfig, full_text: str, missing: list[str]) -> str:
    print(f"⚠ Доправка: добавляем {len(missing)} пропущенных ключа(ей)...")

    relevant_paras = _find_relevant_paragraphs(full_text, missing)
    if not relevant_paras:
        return full_text

    fragment = "\n\n".join(relevant_paras)
    system = (
        "Ты редактор. Получаешь фрагмент статьи и список недостающих ключевых фраз. "
        "Вставь фразы органично — минимальными правками, не меняй стиль. "
        "Верни ТОЛЬКО исправленный фрагмент, без пояснений."
    )
    user = (
        f"Недостающие ключевые фразы: {', '.join(missing)}.\n\n"
        f"Фрагмент для правки:\n{fragment}"
    )

    patched_fragment = call_yandexgpt(config, system, user, temperature=0.2)
    patched_paras = [p.strip() for p in patched_fragment.split("\n\n") if p.strip()]

    result = full_text
    if len(patched_paras) < len(relevant_paras):
        # Подстрахуемся: если модель вернула меньше абзацев, заменим единым блоком.
        return result.replace(fragment, patched_fragment.strip(), 1)

    for original_para, patched_para in zip(relevant_paras, patched_paras):
        result = result.replace(original_para, patched_para, 1)

    return result


def generate_article(config: AppConfig, yaml_path: str, output_path: str = "article_output.md") -> str:
    print("\n=== Запуск генератора ===\n")

    brief = load_brief(yaml_path)
    system, user = build_prompt(brief)
    article = call_yandexgpt(config, system, user)

    must_use = brief["keywords"]["must_use"]
    found, missing = validate_keywords(article, must_use)
    print(f"✓ must-use ключей найдено: {len(found)}/{len(must_use)}")

    should_use = brief["keywords"].get("should_use", [])
    constraints = brief.get("constraints", {})
    should_target = constraints.get("should_use_total", 5) if should_use else 0
    should_count = count_should_use(article, should_use)

    if should_use:
        print(f"✓ should-use вхождений: {should_count} (нужно ≥ {should_target})")
    else:
        print("✓ should-use: список пуст, проверка пропущена")

    to_patch_raw = list(missing)
    if should_use and should_count < should_target:
        text_lemmas = _lemmatize_tokens(_tokenize(article))
        missing_should = [p for p in should_use if not _phrase_in_text_lemmatized(p, text_lemmas)]
        to_patch_raw.extend(missing_should[:2])

    to_patch = list(dict.fromkeys(to_patch_raw))

    if 0 < len(to_patch) <= 2:
        article = patch_missing_keywords(config, article, to_patch)
        found, missing = validate_keywords(article, must_use)
        should_count = count_should_use(article, should_use)
        should_msg = f", should-use: {should_count}" if should_use else ""
        print(f"✓ После доправки — must-use: {len(found)}/{len(must_use)}{should_msg}")
    elif len(to_patch) > 2:
        print(f"✗ Пропущено много фраз ({len(to_patch)}) — рекомендуется перегенерация")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(article)
    print(f"\n✓ Статья сохранена: «{output_path}»")

    if missing:
        print(f"⚠ Всё ещё отсутствуют: {missing}")
    else:
        print("✓ Все обязательные ключи присутствуют!")

    return article


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SEO-генератор статей через YandexGPT")
    parser.add_argument("--brief", default="brief.yaml", help="Путь к YAML-брифу")
    parser.add_argument("--out", default="article_output.md", help="Путь к итоговому Markdown")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config_from_env()
    generate_article(config, args.brief, args.out)


if __name__ == "__main__":
    main()
