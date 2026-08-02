"""Content preprocessing: turns a list of crawled pages into one clean,
word-budget-safe context string for the AI prompt.

Crawl4AI already strips nav/script/style tags at the source (see the
`excluded_tags` config in `crawl4ai_client.py`); this module removes what
Crawl4AI's markdown conversion typically leaves behind — cookie-banner
boilerplate and paragraphs duplicated across pages (shared footers, legal
blurbs) — then caps the combined word count so the AI prompt never
exceeds `max_words`.
"""

from __future__ import annotations

import re

from app.crawler.types import CrawledPage

_COOKIE_BANNER_PATTERNS = (
    re.compile(r"(?i)we use cookies.{0,200}?(accept|agree|got it)"),
    re.compile(r"(?i)this (web)?site uses cookies.{0,200}?(accept|agree|got it)"),
    re.compile(r"(?i)by (continuing|using this site).{0,150}?cookies"),
)

_WHITESPACE_RE = re.compile(r"[ \t]+")
_BLANK_LINES_RE = re.compile(r"\n{3,}")


def clean_page_text(text: str) -> str:
    """Strip cookie-banner boilerplate and collapse excess whitespace from
    one page's already-markdown-ified content."""
    cleaned = text
    for pattern in _COOKIE_BANNER_PATTERNS:
        cleaned = pattern.sub("", cleaned)
    cleaned = _WHITESPACE_RE.sub(" ", cleaned)
    cleaned = _BLANK_LINES_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def _paragraphs(text: str) -> list[str]:
    return [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]


def build_research_context(pages: list[CrawledPage], *, max_words: int) -> str:
    """Combine multiple crawled pages into one deduplicated, word-capped
    context block ready to hand to the AI prompt. Paragraphs repeated
    across pages (e.g. a shared footer) are kept only once."""
    seen_paragraphs: set[str] = set()
    sections: list[str] = []
    word_count = 0

    for page in pages:
        cleaned = clean_page_text(page.text_content)
        unique_paragraphs = []
        for paragraph in _paragraphs(cleaned):
            key = paragraph.lower()
            if key in seen_paragraphs:
                continue
            seen_paragraphs.add(key)
            unique_paragraphs.append(paragraph)

        if not unique_paragraphs:
            continue

        page_text = "\n\n".join(unique_paragraphs)
        page_word_count = len(page_text.split())

        if word_count + page_word_count > max_words:
            remaining = max_words - word_count
            if remaining <= 0:
                break
            page_text = " ".join(page_text.split()[:remaining])
            page_word_count = remaining

        section_header = f"## Source: {page.title or page.url} ({page.url})"
        sections.append(f"{section_header}\n\n{page_text}")
        word_count += page_word_count

        if word_count >= max_words:
            break

    return "\n\n---\n\n".join(sections)
