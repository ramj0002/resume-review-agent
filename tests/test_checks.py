from resume_review.checks import (
    buzzwords,
    bullets_without_numbers,
    impossible_percentages,
    inconsistent_figures,
)


def test_flags_impossible_percentage():
    findings = impossible_percentages("60% of 4 first-time users hit problems")
    assert len(findings) == 1
    assert "2.4" in findings[0].detail


def test_allows_possible_percentage():
    assert impossible_percentages("50% of 4 users and 60% of 100 respondents") == []


def test_finds_buzzwords():
    words = [f.detail for f in buzzwords("Analytical and detail-oriented team player")]
    assert any("analytical" in w for w in words)
    assert any("detail-oriented" in w for w in words)
    assert any("team player" in w for w in words)


def test_bullets_without_numbers_joins_wrapped_lines():
    text = "• Built a dashboard for\n  managers\n• Cut costs by 20%\n"
    findings = bullets_without_numbers(text)
    assert len(findings) == 1
    assert "managers" in findings[0].detail


def test_inconsistent_figures():
    resume = "accuracy reached 94.3% on CT"
    master = "accuracy reached 94.81% on CT"
    findings = inconsistent_figures(resume, master)
    assert len(findings) == 1
    assert "94.81" in findings[0].detail


def test_finds_corporate_phrases():
    words = [f.detail for f in buzzwords("Interested in leveraging AI to drive digital transformation and deliver meaningful impact")]
    assert any("leveraging" in w for w in words)
    assert any("drive digital transformation" in w for w in words)
    assert any("meaningful impact" in w for w in words)
