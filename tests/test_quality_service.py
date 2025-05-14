import pytest
from datetime import datetime
from data_mesh.quality.quality_service import (
    DataQualityService,
    QualityRule,
    QualityCheck
)

@pytest.fixture
def quality_service():
    """Fixture to create a fresh quality service instance for each test."""
    return DataQualityService()

@pytest.fixture
def sample_rule():
    """Fixture to create a sample quality rule."""
    return QualityRule(
        name="test_completeness",
        description="Test completeness rule",
        rule_type="completeness",
        parameters={"required_fields": ["id", "name", "value"]},
        severity="critical"
    )

def test_add_rule(quality_service, sample_rule):
    """Test adding a quality rule."""
    quality_service.add_rule(sample_rule)
    assert sample_rule.name in quality_service.rules
    assert quality_service.rules[sample_rule.name] == sample_rule

def test_remove_rule(quality_service, sample_rule):
    """Test removing a quality rule."""
    quality_service.add_rule(sample_rule)
    quality_service.remove_rule(sample_rule.name)
    assert sample_rule.name not in quality_service.rules

def test_run_quality_check_completeness_pass(quality_service, sample_rule):
    """Test running a completeness check that passes."""
    quality_service.add_rule(sample_rule)
    data = {"id": 1, "name": "test", "value": 100}
    results = quality_service.run_quality_check(data)
    assert len(results) == 1
    assert results[0].passed
    assert "All required fields present" in results[0].message

def test_run_quality_check_completeness_fail(quality_service, sample_rule):
    """Test running a completeness check that fails."""
    quality_service.add_rule(sample_rule)
    data = {"id": 1, "name": "test"}  # Missing 'value' field
    results = quality_service.run_quality_check(data)
    assert len(results) == 1
    assert not results[0].passed
    assert "Missing required fields" in results[0].message
    assert "value" in results[0].details["missing_fields"]

def test_get_check_history(quality_service, sample_rule):
    """Test retrieving check history."""
    quality_service.add_rule(sample_rule)
    data = {"id": 1, "name": "test", "value": 100}
    quality_service.run_quality_check(data)
    history = quality_service.get_check_history(sample_rule.name)
    assert len(history) == 1
    assert isinstance(history[0], QualityCheck)

def test_get_quality_metrics(quality_service, sample_rule):
    """Test retrieving quality metrics."""
    quality_service.add_rule(sample_rule)
    data = {"id": 1, "name": "test", "value": 100}
    quality_service.run_quality_check(data)
    metrics = quality_service.get_quality_metrics()
    assert metrics["total_checks"] == 1
    assert metrics["passed_checks"] == 1
    assert metrics["pass_rate"] == 100.0
    assert metrics["active_rules"] == 1

def test_unknown_rule_type(quality_service):
    """Test handling of unknown rule type."""
    rule = QualityRule(
        name="test_unknown",
        description="Test unknown rule type",
        rule_type="unknown_type",
        parameters={},
        severity="critical"
    )
    quality_service.add_rule(rule)
    with pytest.raises(ValueError, match="Unknown rule type"):
        quality_service.run_quality_check({}) 