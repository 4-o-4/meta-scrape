from __future__ import annotations

from typing import Callable
from urllib.parse import urlparse

from scrape.xxx import scrape_xxx

Scraper = Callable[[str], list[dict[str, object]]]

_REGISTRY: dict[str, Scraper] = {
    "xxx": scrape_xxx,
}


def _extract_domain(url: str) -> str:
    hostname = urlparse(url).hostname
    if not hostname:
        raise ValueError(f"Не удалось извлечь домен из URL: {url!r}")
    parts = hostname.split(".")
    return parts[-2] if len(parts) >= 2 else parts[0]


def get_scraper(url: str) -> Scraper:
    domain = _extract_domain(url)
    scraper = _REGISTRY.get(domain)
    if scraper is None:
        available = ", ".join(sorted(_REGISTRY))
        raise ValueError(
            f"Нет scraper-а для домена {domain!r}. "
            f"Доступные: {available}"
        )
    return scraper
