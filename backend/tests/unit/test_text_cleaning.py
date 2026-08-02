"""Unit tests for content preprocessing (app.utils.text_cleaning)."""

from __future__ import annotations

from app.crawler.types import CrawledPage
from app.utils.text_cleaning import build_research_context, clean_page_text


def test_clean_page_text_strips_cookie_banner() -> None:
    text = "We use cookies to improve your experience. Accept\n\nReal content here."
    cleaned = clean_page_text(text)

    assert "cookies" not in cleaned.lower()
    assert "Real content here." in cleaned


def test_clean_page_text_collapses_whitespace() -> None:
    text = "Too    many     spaces\n\n\n\n\nand blank lines."
    cleaned = clean_page_text(text)

    assert "Too many spaces" in cleaned
    assert "\n\n\n" not in cleaned


def test_build_research_context_deduplicates_repeated_paragraphs() -> None:
    shared_footer = "© 2026 Example Corp. All rights reserved."
    pages = [
        CrawledPage(
            url="https://example.com/",
            title="Home",
            text_content=f"Welcome home.\n\n{shared_footer}",
        ),
        CrawledPage(
            url="https://example.com/about",
            title="About",
            text_content=f"About us.\n\n{shared_footer}",
        ),
    ]

    context = build_research_context(pages, max_words=1000)

    assert context.count(shared_footer) == 1
    assert "Welcome home." in context
    assert "About us." in context


def test_build_research_context_respects_max_words() -> None:
    long_text = " ".join(f"word{i}" for i in range(500))
    pages = [CrawledPage(url="https://example.com/", title="Home", text_content=long_text)]

    context = build_research_context(pages, max_words=50)

    # Header line adds a few extra words ("## Source: ..."), so allow slack.
    assert len(context.split()) <= 60


def test_build_research_context_skips_empty_pages() -> None:
    pages = [
        CrawledPage(url="https://example.com/empty", title="Empty", text_content=""),
        CrawledPage(url="https://example.com/real", title="Real", text_content="Actual content."),
    ]

    context = build_research_context(pages, max_words=1000)

    assert "Actual content." in context
    assert "empty" not in context.lower()
