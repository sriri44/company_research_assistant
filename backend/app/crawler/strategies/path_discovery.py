"""Path discovery strategy for the company-site crawl.

Decides which pages of a company's website are worth crawling: a fixed,
priority-ordered set of high-signal seed paths (home, about, products,
...), plus filtering of internal links discovered while crawling so we
only follow more pages that match the same allow-list. Login/signup/legal
pages and duplicates are explicitly excluded — see docs for this phase.
"""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

SEED_PATHS: tuple[str, ...] = (
    "/",
    "/about",
    "/products",
    "/services",
    "/solutions",
    "/pricing",
    "/contact",
    "/team",
    "/company",
)

_ALLOWED_PATH_KEYWORDS = (
    "about",
    "product",
    "service",
    "solution",
    "pricing",
    "contact",
    "team",
    "company",
)

_BLOCKED_PATH_KEYWORDS = (
    "login",
    "signin",
    "sign-in",
    "signup",
    "sign-up",
    "register",
    "privacy",
    "terms",
    "cookie",
    "cart",
    "checkout",
    "account",
)


def normalize_root_url(domain_or_url: str) -> str:
    """Normalize a bare domain or URL into a fully-qualified `scheme://host` root."""
    candidate = domain_or_url.strip()
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"
    parsed = urlparse(candidate)
    return f"{parsed.scheme}://{parsed.netloc}"


def build_seed_urls(root_url: str) -> list[str]:
    """The fixed set of candidate pages, in priority order, for a domain."""
    return [
        root_url + "/" if path == "/" else urljoin(root_url + "/", path.lstrip("/"))
        for path in SEED_PATHS
    ]


def is_allowed_path(path: str) -> bool:
    """Whether a URL path is worth crawling: on the allow-list and not on
    the block-list. The homepage (`/` or empty) is always allowed."""
    lowered = path.lower()
    if any(blocked in lowered for blocked in _BLOCKED_PATH_KEYWORDS):
        return False
    if path in ("", "/"):
        return True
    return any(keyword in lowered for keyword in _ALLOWED_PATH_KEYWORDS)


def filter_internal_links(base_url: str, hrefs: list[str], *, already_seen: set[str]) -> list[str]:
    """Resolve relative hrefs against `base_url`, keep only same-domain,
    allow-listed, not-already-seen pages, and de-duplicate (trailing
    slash/query/fragment differences collapse to the same page)."""
    base_netloc = urlparse(base_url).netloc
    filtered: list[str] = []

    for href in hrefs:
        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        if parsed.netloc != base_netloc:
            continue
        if not is_allowed_path(parsed.path):
            continue

        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}" or base_url
        if normalized in already_seen:
            continue

        already_seen.add(normalized)
        filtered.append(normalized)

    return filtered
