from msgspec import Struct


class SearchResult(Struct, frozen=True):
    title: str
    name: str


Search = list[SearchResult]
