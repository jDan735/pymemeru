from msgspec import convert
from selectolax.lexbor import LexborHTMLParser

from .aioget import aioget
from .models import Page, Trending


async def page(name: str) -> Page:
    _, page = await aioget(f"https://memepedia.ru/{name}/")

    sel = LexborHTMLParser(page)
    post = sel.css_first(".s-post-main")

    try:
        image = post.css_first("figure.post-thumbnail img").attributes.get("src")
    except Exception:
        image = post.css_first("div.bb-media-placeholder img").attributes.get("src")

    try:
        trending_ = sel.css(".widget_trending_entries ul")
    except Exception:
        trending_ = []

    try:
        comments = sel.css_first("a.post-comments span.count").text()
    except Exception:
        comments = "0"

    _ = Page(
        title=post.css_first("h1").text(),
        published_at=post.css_first("time.published").text(),
        author_name=sel.css_first("div.author-info a.auth-url span").text(),
        views=(sel.css_first("span.post-views span.count").text()),
        comments=comments,
        main_image=image,
        text=post.html,
        trending=[
            Trending(
                preview=trending.css_first("img").attributes.get("src"),
                title=trending.css_first(".content a").text(),
                url="/"
                + trending.css_first(".content a").attributes["href"].split("/")[-2],
            )
            for trending in trending_
        ],
    )

    return convert(_, Page)
