from src.preprocessing import clean_text


def test_clean_text_strips_and_collapses_whitespace():
    assert clean_text("  halo   dunia \n") == "halo dunia"


def test_clean_text_handles_non_string():
    assert clean_text(None) == ""
