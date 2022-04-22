import sys
sys.path.insert(0, ".")


import pytest
import pymemeru


class TestPopular:
    @pytest.mark.asyncio
    async def test_popular(self):
        pages = await pymemeru.popular()

        assert isinstance(pages, list)
        assert len(pages) > 0
