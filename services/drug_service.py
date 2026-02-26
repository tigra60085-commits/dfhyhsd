"""Сервис для работы с информацией о препаратах."""
from typing import Dict, List, Optional
from data.drugs import DRUGS_DATA


class DrugService:
    """Сервис для получения информации о препаратах."""

    @staticmethod
    def get_drug_info(drug_name: str) -> Optional[Dict]:
        """Получить информацию о препарате по названию."""
        return DRUGS_DATA.get(drug_name.lower())

    @staticmethod
    def search_drugs(query: str) -> List[str]:
        """Поиск препаратов по частичному совпадению названия."""
        query = query.lower()
        return [
            drug_name for drug_name in DRUGS_DATA.keys()
            if query in drug_name.lower()
        ]

    @staticmethod
    def get_all_drugs() -> List[str]:
        """Получить список всех доступных препаратов."""
        return list(DRUGS_DATA.keys())