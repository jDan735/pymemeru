from pydantic import BaseModel, RootModel


class SearchResult(BaseModel):
    title: str
    name: str


Search = RootModel[list[SearchResult]]
