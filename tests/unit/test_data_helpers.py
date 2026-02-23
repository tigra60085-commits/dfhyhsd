"""Unit tests for data module helper functions."""

import pytest

from data.drugs import get_drugs_by_class, get_drug_by_name, search_drugs, fuzzy_suggest
from data.quiz_questions import get_questions_by_category, get_filtered_questions
from data.interactions import find_interaction, find_interactions_for_drug
from data.clinical_cases import get_case_by_id


class TestDrugs:
    """Tests for data.drugs functions."""

    def test_get_drugs_by_class_ssri(self):
        """Valid class should return list of drug dicts."""
        drugs = get_drugs_by_class("SSRI")
        assert isinstance(drugs, list)
        assert len(drugs) > 0
        for drug in drugs:
            assert "name" in drug
            assert "class" in drug
            assert "mechanism" in drug
            assert drug["class"] == "SSRI"

    def test_get_drugs_by_class_nonexistent(self):
        """Nonexistent class should return empty list."""
        drugs = get_drugs_by_class("NonExistentClass")
        assert drugs == []

    def test_get_drugs_by_class_ansiolitics(self):
        """Anxiolytics class should have multiple drugs."""
        drugs = get_drugs_by_class("Анксиолитики")
        assert len(drugs) >= 3

    def test_get_drug_by_name_exact(self):
        """Exact match should return drug dict."""
        drug = get_drug_by_name("Флуоксетин")
        assert drug is not None
        assert drug["name"] == "Флуоксетин"
        assert "class" in drug
        assert "mechanism" in drug

    def test_get_drug_by_name_case_insensitive(self):
        """Name match should be case-insensitive."""
        drug1 = get_drug_by_name("ФЛУОКСЕТИН")
        drug2 = get_drug_by_name("флуоксетин")
        drug3 = get_drug_by_name("Флуоксетин")
        assert drug1 is not None
        assert drug2 is not None
        assert drug3 is not None
        assert drug1["name"] == drug2["name"] == drug3["name"]

    def test_get_drug_by_name_nonexistent(self):
        """Nonexistent drug should return None."""
        drug = get_drug_by_name("DrugThatDoesNotExist")
        assert drug is None

    def test_search_drugs_by_indication(self):
        """Search should find drugs by indication."""
        results = search_drugs("депрессия")
        assert len(results) > 0
        # Должны быть SSRI в результатах
        assert any(d["class"] == "SSRI" for d in results)

    def test_search_drugs_by_class(self):
        """Search should find drugs by class name."""
        results = search_drugs("SSRI")
        assert len(results) > 0
        assert all(d["class"] == "SSRI" for d in results)

    def test_fuzzy_suggest_typo(self):
        """Fuzzy suggest should find similar drug names."""
        suggestions = fuzzy_suggest("флуокс")
        assert "Флуоксетин" in suggestions


class TestQuizQuestions:
    """Tests for data.quiz_questions functions."""

    def test_get_questions_by_category_none(self):
        """None category should return all questions."""
        questions = get_questions_by_category(None)
        assert isinstance(questions, list)

    def test_get_questions_structure(self):
        """Questions should have required fields when present."""
        questions = get_questions_by_category(None)
        if len(questions) > 0:
            for q in questions:
                assert "question" in q
                assert "options" in q
                assert "correct" in q
                assert "explanation" in q
                assert len(q["options"]) >= 2
                assert isinstance(q["correct"], int)

    def test_get_filtered_questions_correct_params(self):
        """get_filtered_questions with correct param names."""
        questions = get_filtered_questions(category="all", difficulty="easy")
        assert isinstance(questions, list)


class TestInteractions:
    """Tests for data.interactions functions."""

    def test_find_interaction_exists(self):
        """Existing interaction should be found."""
        results = find_interaction("SSRI", "MAOI")
        assert len(results) > 0
        assert all("severity" in r and "description" in r for r in results)

    def test_find_interaction_reversed(self):
        """Reversed order of drug pair should still find result."""
        results1 = find_interaction("MAOI", "SSRI")
        results2 = find_interaction("SSRI", "MAOI")
        assert len(results1) > 0
        assert len(results2) > 0

    def test_find_interaction_nonexistent(self):
        """Unknown drug pair should return empty list."""
        results = find_interaction("UnknownDrug1", "UnknownDrug2")
        assert results == []

    def test_find_interactions_for_drug_ssri(self):
        """SSRI should have multiple interactions."""
        results = find_interactions_for_drug("SSRI")
        assert len(results) > 0

    def test_find_interactions_for_drug_nonexistent(self):
        """Nonexistent drug may return empty."""
        results = find_interactions_for_drug("DrugNotInData")
        assert isinstance(results, list)


class TestClinicalCases:
    """Tests for data.clinical_cases functions."""

    def test_get_case_by_id_valid(self):
        """Valid case ID should return case dict."""
        case = get_case_by_id(1)
        assert case is not None
        assert "id" in case
        assert "title" in case
        assert "question" in case
        assert "options" in case
        assert "correct" in case
        assert "explanation" in case

    def test_get_case_by_id_multiple(self):
        """Multiple case IDs should work."""
        case1 = get_case_by_id(1)
        case2 = get_case_by_id(2)
        assert case1 is not None
        assert case2 is not None
        assert case1["id"] != case2["id"]

    def test_get_case_by_id_invalid(self):
        """Invalid case ID should return None."""
        case = get_case_by_id(9999)
        assert case is None
