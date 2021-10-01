import sys
sys.path.insert(0, ".")


import pytest
from pymemeru.page import page


class TestSearch:
    @pytest.mark.asyncio
    async def test_search(self):
        res = await page("test-kak-xorosho-ty-znaesh-memy-pro-shkolnikov")
