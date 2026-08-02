"""Unit tests for crawl path discovery (app.crawler.strategies.path_discovery)."""

from __future__ import annotations

from app.crawler.strategies.path_discovery import (
    build_seed_urls,
    filter_internal_links,
    is_allowed_path,
    normalize_root_url,
)


def test_normalize_root_url_adds_scheme() -> None:
    assert normalize_root_url("example.com") == "https://example.com"


def test_normalize_root_url_strips_path() -> None:
    assert normalize_root_url("https://example.com/some/deep/page") == "https://example.com"


def test_build_seed_urls_includes_homepage_and_allowed_paths() -> None:
    urls = build_seed_urls("https://example.com")

    assert "https://example.com/" in urls
    assert any(url.endswith("/about") for url in urls)
    assert any(url.endswith("/pricing") for url in urls)
    assert len(urls) == len(set(urls))  # no duplicates


def test_is_allowed_path_accepts_allow_listed_paths() -> None:
    assert is_allowed_path("/about")
    assert is_allowed_path("/products/widgets")
    assert is_allowed_path("/")


def test_is_allowed_path_rejects_blocked_paths() -> None:
    assert not is_allowed_path("/login")
    assert not is_allowed_path("/signup")
    assert not is_allowed_path("/privacy-policy")
    assert not is_allowed_path("/cart/checkout")


def test_is_allowed_path_rejects_unlisted_paths() -> None:
    assert not is_allowed_path("/blog/some-post")
    assert not is_allowed_path("/careers")


def test_filter_internal_links_excludes_external_domains() -> None:
    seen: set[str] = set()
    links = filter_internal_links(
        "https://example.com",
        ["https://example.com/about", "https://other-site.com/about"],
        already_seen=seen,
    )

    assert links == ["https://example.com/about"]


def test_filter_internal_links_deduplicates_against_already_seen() -> None:
    seen = {"https://example.com/about"}
    links = filter_internal_links("https://example.com", ["/about", "/pricing"], already_seen=seen)

    assert links == ["https://example.com/pricing"]


def test_filter_internal_links_rejects_blocked_paths() -> None:
    seen: set[str] = set()
    links = filter_internal_links("https://example.com", ["/login", "/products"], already_seen=seen)

    assert links == ["https://example.com/products"]
