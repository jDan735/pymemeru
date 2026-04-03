from msgspec import Struct
from bs4 import BeautifulSoup
from selectolax.lexbor import LexborHTMLParser, LexborNode, create_tag


def stripped_strings(node: LexborNode):
    for desc in node.traverse(include_text=True):
        if desc.is_text_node:
            text = desc.text().strip()

            if text:
                yield text


class Trending(Struct, frozen=True):
    preview: str
    title: str
    url: str

    views: str = "0"


class Page(Struct, frozen=True):
    title: str
    published_at: str

    views: str
    comments: str

    author_name: str

    main_image: str
    text: str
    trending: list[Trending]

    @property
    def cleared_text(self) -> str:
        sel = LexborHTMLParser(self.text)

        for tag in [
            *sel.css("time"),
            *sel.css("img.avatar"),
            *sel.css("span.count"),
            *sel.css('span[itemprop="name"]'),
            *sel.css("div.mistape_caption, div.share-box"),
            *sel.css("h1"),
            *sel.css("hr"),
            *sel.css("figure.bb-mb-el"),
            *sel.css("div.tds-message-box"),
            *sel.css("div.clearfix"),
            *sel.css("div.twitter-tweet"),
        ]:
            tag.replace_with("")

        for tag in sel.css("div.su-quote-inner"):
            new_tag = create_tag("blockquoter")
            new_tag.insert_child(tag.inner_html)

            tag.replace_with(new_tag)

        for tag in sel.css("span.su-quote-cite"):
            new_tag = create_tag("cite")
            new_tag.insert_child(tag.inner_html)

            tag.replace_with(new_tag)

        for tag in sel.css("h2"):
            if tag.text() in ("Галерея", "Читайте также"):
                tag.replace_with("")

        for tag in sel.css("a"):
            if tag.attrs["href"] == "https://t.me/memepedia_Ru":
                tag.replace_with("")

        for tag in sel.css("div.wc-comment-text"):
            tag.replace_with(
                LexborHTMLParser(
                    "\n\n".join(
                        map(
                            lambda x: f"<blockquote>{x}</blockquote>",
                            stripped_strings(tag),
                        )
                    )
                ).root
                or ""
            )

        # for tag in sel.css("em"):
        #     _ = LexborHTMLParser(f"<blockquote>{tag.text()}</blockquote>")
        #     tag.replace_with(_.root or "")

        for tag in sel.css("h2"):
            _ = LexborHTMLParser(f"<b>{tag.text()}</b>\n")
            tag.replace_with(_.root or "")

        for tag in sel.css("a"):
            if tag.attrs.get("href", "").startswith("https://memepedia.ru/"):
                tag.attrs["href"] = "/memepedia/" + tag.attrs.get(
                    "href", ""
                ).removeprefix("https://memepedia.ru/")

        return sel.html
