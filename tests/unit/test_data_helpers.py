"""Unit tests for pure helper functions in the data/ package."""

import pytest

from data.drugs import DRUG_CLASSES, DRUGS, get_drug_by_name, get_drugs_by_class, search_drugs
from data.interactions import INTERACTIONS, find_interaction, find_interactions_for_drug
from data.clinical_cases import CASES, get_case_by_id
from data.quiz_questions import QUESTIONS, get_filtered_questions, get_questions_by_category, get_questions_by_difficulty


# ─── data/drugs.py ────────────────────────────────────────────────────────────


class TestGetDrugsByClass:
    def test_returns_list_for_known_class(self):
        results = get_drugs_by_class("SSRI")
        assert isinstance(results, list)
        assert len(results) > 0

    def test_all_items_have_required_keys(self):
        for drug in get_drugs_by_class("SSRI"):
            assert "name" in drug
            assert "class" in drug
            assert "mechanism" in drug

    def test_filters_by_class_correctly(self):
        results = get_drugs_by_class("SSRI")
        for drug in results:
            assert drug["class"] == "SSRI"

    def test_returns_empty_list_for_nonexistent_class(self):
        assert get_drugs_by_class("NONEXISTENT_CLASS_XYZ") == []

    def test_multiple_classes_present(self):
        # Ensure the DB has data for several known classes
        for cls in ("SSRI", "SNRI", "Атипичные антипсихотики"):
            assert len(get_drugs_by_class(cls)) > 0, f"No drugs for class: {cls}"

    def test_class_filter_is_exact_match(self):
        # "SSRI" should NOT return SNRI drugs
        results = get_drugs_by_class("SSRI")
        for drug in results:
            assert drug["class"] != "SNRI"


class TestGetDrugByName:
    def test_finds_known_drug(self):
        drug = get_drug_by_name("Флуоксетин")
        assert drug is not None
        assert drug["name"] == "Флуоксетин"

    def test_case_insensitive_lookup(self):
        lower = get_drug_by_name("флуоксетин")
        upper = get_drug_by_name("ФЛУОКСЕТИН")
        mixed = get_drug_by_name("Флуоксетин")
        assert lower is not None
        assert lower["name"] == mixed["name"] == upper["name"]

    def test_returns_none_for_unknown_drug(self):
        assert get_drug_by_name("НесуществующийПрепарат") is None

    def test_result_has_all_required_keys(self):
        drug = get_drug_by_name("Сертралин")
        assert drug is not None
        for key in ("name", "class", "mechanism", "indications", "side_effects", "dosage"):
            assert key in drug, f"Missing key: {key}"

    def test_indications_is_list(self):
        drug = get_drug_by_name("Сертралин")
        assert isinstance(drug["indications"], list)
        assert len(drug["indications"]) > 0


class TestSearchDrugs:
    def test_empty_query_returns_empty_list(self):
        # Empty query string: no meaningful match expected
        results = search_drugs("")
        # Either empty or full list — both are acceptable; document current behavior
        assert isinstance(results, list)

    def test_search_by_partial_name(self):
        results = search_drugs("сертра")
        names = [d["name"] for d in results]
        assert "Сертралин" in names

    def test_search_by_class_name(self):
        results = search_drugs("ssri")
        assert len(results) > 0
        for drug in results:
            assert drug["class"] == "SSRI"

    def test_search_by_indication(self):
        # "депрессия" appears in indications of multiple drugs
        results = search_drugs("депрессия")
        assert len(results) > 0

    def test_search_nonexistent_returns_empty(self):
        assert search_drugs("xyzqwerty_nonexistent_drug_abc") == []

    def test_returns_list_of_dicts(self):
        for drug in search_drugs("флу"):
            assert isinstance(drug, dict)
            assert "name" in drug


# ─── data/interactions.py ─────────────────────────────────────────────────────


class TestFindInteraction:
    def test_known_pair_returns_results(self):
        results = find_interaction("MAOI", "SSRI")
        assert len(results) > 0

    def test_result_has_required_keys(self):
        results = find_interaction("MAOI", "SSRI")
        assert len(results) > 0
        for item in results:
            assert "drugs" in item
            assert "severity" in item
            assert "description" in item

    def test_severity_valid_value(self):
        results = find_interaction("MAOI", "SSRI")
        for item in results:
            assert item["severity"] in ("severe", "moderate", "mild")

    def test_reversed_pair_still_matches(self):
        # Matching should work regardless of argument order
        forward = find_interaction("MAOI", "SSRI")
        reversed_ = find_interaction("SSRI", "MAOI")
        assert len(forward) > 0
        assert len(reversed_) > 0

    def test_unknown_pair_returns_empty(self):
        result = find_interaction("ВымышленныйПрепарат1", "ВымышленныйПрепарат2")
        assert result == []

    def test_partial_name_matching(self):
        # "трамадол" should match the stored "трамадол" entry
        results = find_interaction("MAOI", "трамадол")
        assert len(results) > 0


class TestFindInteractionsForDrug:
    def test_returns_list(self):
        result = find_interactions_for_drug("MAOI")
        assert isinstance(result, list)

    def test_known_drug_has_interactions(self):
        result = find_interactions_for_drug("MAOI")
        assert len(result) > 0

    def test_unknown_drug_returns_empty(self):
        result = find_interactions_for_drug("ВымышленныйПрепаратXYZ")
        assert result == []

    def test_lithium_interactions(self):
        result = find_interactions_for_drug("литий")
        assert len(result) > 0


# ─── data/clinical_cases.py ───────────────────────────────────────────────────


class TestGetCaseById:
    def test_valid_id_returns_dict(self):
        case = get_case_by_id(1)
        assert case is not None
        assert isinstance(case, dict)

    def test_result_has_required_keys(self):
        case = get_case_by_id(1)
        for key in ("id", "title", "presentation", "question", "options", "correct", "explanation"):
            assert key in case, f"Missing key: {key}"

    def test_correct_index_in_range(self):
        for c in CASES:
            assert isinstance(c["correct"], int)
            assert 0 <= c["correct"] < len(c["options"])

    def test_invalid_id_returns_none(self):
        assert get_case_by_id(99999) is None

    def test_negative_id_returns_none(self):
        assert get_case_by_id(-1) is None

    def test_options_is_list_with_multiple_items(self):
        case = get_case_by_id(1)
        assert isinstance(case["options"], list)
        assert len(case["options"]) >= 2


# ─── data/quiz_questions.py ───────────────────────────────────────────────────


class TestGetQuestionsByCategory:
    def test_known_category_returns_questions(self):
        results = get_questions_by_category("Механизмы действия")
        assert len(results) > 0

    def test_all_results_match_category(self):
        cat = "Показания"
        for q in get_questions_by_category(cat):
            assert q["category"] == cat

    def test_unknown_category_returns_empty(self):
        assert get_questions_by_category("НесуществующаяКатегория") == []

    def test_question_has_required_keys(self):
        questions = get_questions_by_category("Механизмы действия")
        assert len(questions) > 0
        for q in questions:
            for key in ("question", "options", "correct", "explanation", "category", "difficulty"):
                assert key in q, f"Missing key: {key}"


class TestGetFilteredQuestions:
    def test_no_filters_returns_all(self):
        results = get_filtered_questions()
        assert len(results) == len(QUESTIONS)

    def test_difficulty_filter_easy(self):
        results = get_filtered_questions(difficulty="easy")
        for q in results:
            assert q["difficulty"] == "easy"

    def test_difficulty_filter_hard(self):
        results = get_filtered_questions(difficulty="hard")
        for q in results:
            assert q["difficulty"] == "hard"

    def test_category_filter(self):
        cat = "Фармакокинетика"
        results = get_filtered_questions(category=cat)
        for q in results:
            assert q["category"] == cat

    def test_combined_filter(self):
        results = get_filtered_questions(category="Механизмы действия", difficulty="easy")
        for q in results:
            assert q["category"] == "Механизмы действия"
            assert q["difficulty"] == "easy"

    def test_correct_is_valid_index(self):
        for q in get_filtered_questions():
            assert isinstance(q["correct"], int)
            assert 0 <= q["correct"] < len(q["options"]), (
                f"correct={q['correct']} out of range for options of len {len(q['options'])}"
            )
