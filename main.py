from __future__ import annotations

import json
import sys

from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver

from scraper_factory import get_scraper


def main() -> None:
    urls = sys.argv[1:]
    if not urls:
        sys.exit(1)

    scraper = get_scraper(urls[0])
    driver = SafariWebDriver()
    try:
        all_scenes: list[list[dict[str, object]]] = []
        for url in urls:
            all_scenes.append(scraper(url, driver=driver))

    finally:
        driver.quit()

    json.dump(all_scenes, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
