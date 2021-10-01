import sys
sys.path.insert(0, ".")


import pytest
from pymemeru.search import search


class TestSearch:
    @pytest.mark.asyncio
    async def test_search(self):
        res = await search("тест")

        assert len(res) == 10
