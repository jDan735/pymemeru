from msgspec import convert
from selectolax.lexbor import LexborHTMLParser

from .aioget import aioget
from .models import Search, SearchResult


async def search(query: str) -> list[SearchResult]:
    _, page = await aioget("https://memepedia.ru", {"s": query})

    sel = LexborHTMLParser(page)
    ul = sel.css_first("ul.post-items")

    results = []

    for li in ul.css("li"):
        article = li.css_first("article")
        content = article.css_first("div.content")

        results.append(
            dict(
                title=content.css_first("header h2 a").text(),
                name=content.css_first("header h2 a").attributes.get("href")[21:-1],
            )
        )

    return convert(results, Search)
