from msgspec import convert
from selectolax.lexbor import LexborHTMLParser

from .aioget import aioget
from .models import Trending


async def popular() -> list[Trending]:
    _, page = await aioget("https://memepedia.ru/memoteka/")
    sel = LexborHTMLParser(page)

    _ = [
        dict(
            preview=trending.css_first("img").attributes["src"],
            title=trending.css_first(".entry-title a").text(),
            url="/"
            + trending.css_first(".entry-title a").attributes["href"].split("/")[-2],
            views=(trending.css_first("span.post-views span.count").text()),
        )
        for trending in sel.css(".post-item")
    ]

    return convert(_, list[Trending])
