from pydantic import BaseModel
from bs4 import BeautifulSoup


class Trending(BaseModel):
    preview: str
    title: str
    url: str

    views: str = "0"


class Page(BaseModel):
    title: str
    published_at: str

    views: str
    comments: str

    author_name: str

    main_image: str
    text: str
    trending: list[Trending]

    @property
    def cleared_text(self) -> BeautifulSoup:
        soup = BeautifulSoup(self.text, features="lxml")

        for tag in [
            *soup.find_all("time"),
            *soup.find_all("img", class_=["avatar"]),
            *soup.find_all("span", class_=["count"]),
            *soup.find_all("span", itemprop="name"),
            *soup.find_all("div", class_=["mistape_caption", "share-box"]),
            *soup.find_all("h1"),
            *soup.find_all("hr"),
            *soup.find_all("figure", class_="bb-mb-el"),
            *soup.find_all("div", class_="tds-message-box"),
        ]:
            tag.replace_with("")

        for tag in soup.find_all("div", class_="su-quote-inner"):
            tag.name = "blockquote"

        for tag in soup.find_all("span", class_="su-quote-cite"):
            tag.name = "cite"

        for tag in soup.find_all("h2"):
            if tag.text in ("Галерея", "Читайте также"):
                tag.replace_with("")

        for tag in soup.find_all("a"):
            if tag["href"] == "https://t.me/memepedia_Ru":
                tag.replace_with("")

        for tag in soup.find_all("div", class_="wc-comment-text"):
            tag.replace_with(
                "\n\n".join(
                    map(
                        lambda x: f"<blockquote>{x}</blockquote>JDAN_EXTRA_SPACE",
                        tag.stripped_strings,
                    )
                )
            )

        for tag in soup.find_all("em", recursive=True):
            tag.replace_with(f"<blockquote>{tag.text}</blockquote>JDAN_EXTRA_SPACE")

        for tag in soup.find_all("a"):
            if tag["href"].startswith("https://memepedia.ru/"):
                tag["href"] = "/memepedia/" + tag["href"].removeprefix(
                    "https://memepedia.ru/"
                )

        return soup
