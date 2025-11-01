import sys
sys.path.insert(0, ".")


import pytest
import pymemeru


class TestPage:
    @pytest.mark.asyncio
    async def test_search(self):
        page = await pymemeru.page("arestovannyj-viktor-medvedchuk")

        assert page.title == "Арестованный Виктор Медведчук"
        assert page.published_at == "13.04.2022 в 09:12"

        assert page.author_name == "Mememother"
        
        assert page.main_image == "https://memepedia.ru/wp-content/uploads/2022/04/photo_2022-04-13_09-29-35.jpg"
        assert page.text != ""

    @pytest.mark.asyncio
    async def test_search2(self):
        page = await pymemeru.page("ne-vse-tak-odnoznachno")

        assert page.title == "Не все так однозначно"
        assert page.published_at == "11.04.2022 в 11:56"

        assert page.author_name == "Mememaster"
        
        assert page.main_image == "https://memepedia.ru/wp-content/uploads/2022/04/vsej-pravdy-my-ne-znaem-mem.jpg"
        assert page.text != ""
