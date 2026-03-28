from __future__ import annotations

from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver

_SOFT_LINE_BREAK = "\u2028"
_NEWLINE = "\u000A"
_NBSP = "\u00a0"
_TARGET_TAGS: set[str] = {"h1", "h2", "h3", "p", "ul"}

ScrapedItem = dict[str, object]


def _tag_to_key(tag: str) -> str:
    tag = tag.lower()
    if tag in {"h1", "h2"}:
        return tag
    if tag in {"h3", "p", "ul"}:
        return "p"
    raise ValueError(f"Неизвестный тег: {tag!r}")


def _syntax_code_text(syntaxhighlighter_el: WebElement) -> str:
    td_code = syntaxhighlighter_el.find_element(By.CSS_SELECTOR, "td.code")
    line_divs = td_code.find_elements(By.CSS_SELECTOR, "div.line")
    lines: list[str] = []
    for line_div in line_divs:
        text = line_div.text.replace(_NBSP, " ")
        lines.append(text)
    return _SOFT_LINE_BREAK.join(lines)


def _process_element(
        el: WebElement,
        out: list[ScrapedItem],
        search_targets: bool = True,
) -> None:
    tag = el.tag_name.lower()

    if search_targets and tag in _TARGET_TAGS:
        if tag == "ul":
            items: list[str] = []
            for li in el.find_elements(By.CSS_SELECTOR, "li"):
                li_text = li.text.strip().replace(_NEWLINE, "")
                if li_text:
                    items.append(li_text)
            if items:
                out.append({"p": items})
        else:
            text = el.text.strip().replace(_NEWLINE, "")
            if text:
                out.append({_tag_to_key(tag): text})
        return

    if tag == "div":
        classes_attr: Optional[str] = el.get_attribute("class")
        classes = (classes_attr or "").split()
        if "syntaxhighlighter" in classes:
            code_text = _syntax_code_text(el).strip()
            if code_text:
                out.append({"code": code_text})
            return

    for child in el.find_elements(By.XPATH, "./*"):
        _process_element(child, out, search_targets=False)


def scrape_xxx(
        url: str,
) -> list[ScrapedItem]:
    driver: WebDriver = SafariWebDriver()
    try:
        driver.get(url)
        content_blocks = driver.find_elements(By.CSS_SELECTOR, "div.item.center.menC")
        out: list[ScrapedItem] = []
        for block in content_blocks:
            for child in block.find_elements(By.XPATH, "./*"):
                _process_element(child, out)
        return out
    finally:
        driver.quit()
