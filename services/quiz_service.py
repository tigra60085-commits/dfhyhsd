"""Сервис для работы с викторинами."""
from typing import Dict, List, Optional
from data.quiz_questions import QUIZ_QUESTIONS


class QuizService:
    """Сервис для управления викторинами."""

    @staticmethod
    def get_random_question(exclude_categories: Optional[List[str]] = None) -> Optional[Dict]:
        """Получить случайный вопрос из доступных."""
        import random
        filtered_questions = QUIZ_QUESTIONS
        if exclude_categories:
            filtered_questions = [
                q for q in QUIZ_QUESTIONS
                if q.get('category') not in exclude_categories
            ]
        return random.choice(filtered_questions) if filtered_questions else None

    @staticmethod
    def check_answer(question: Dict, selected_option: int) -> bool:
        """Проверить правильность ответа."""
        return question['correct_option'] == selected_option

    @staticmethod
    def get_questions_by_category(category: str) -> List[Dict]:
        """Получить все вопросы по категории."""
        return [q for q in QUIZ_QUESTIONS if q.get('category') == category]