"""Integration tests for database query helpers."""

import pytest


@pytest.mark.asyncio
async def test_db_fixture_is_available(db_conn):
    """Test that db_conn fixture is properly created."""
    assert db_conn is not None
    # Verify we can execute queries
    cursor = await db_conn.execute("SELECT COUNT(*) FROM users")
    result = await cursor.fetchone()
    assert result is not None


def test_data_modules_importable():
    """Test that data modules can be imported without errors."""
    from data.drugs import get_drug_by_name, search_drugs
    from data.quiz_questions import get_questions_by_category
    from data.interactions import find_interaction
    from data.clinical_cases import get_case_by_id
    
    # Smoke tests - just verify they can be called
    assert get_drug_by_name("Флуоксетин") is not None
    assert search_drugs("депрессия") is not None
    questions = get_questions_by_category(None)
    assert isinstance(questions, list)
    assert find_interaction("SSRI", "MAOI") is not None
    assert get_case_by_id(1) is not None
