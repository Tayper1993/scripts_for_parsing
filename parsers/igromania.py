import asyncio

import aiohttp
from bs4 import BeautifulSoup as BS

from core.mongodb.connecttion import collection_igromania
from parsers.settings import HEADERS, URL_IGROMANIA


async def parse_igromania_news():
    """
    Парсим сайт с новостями igromania и сохраняем список словарей в MongoDB.
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(URL_IGROMANIA, headers=HEADERS) as response:
            html = await response.text()
            soup = BS(html, 'html.parser')

            items = soup.find_all('div', {'class': 'ShelfCard_card__GrWrN'})
            tasks = []

            for item in items:
                all_elements = item.find('a')
                link = all_elements['href']

                task = asyncio.create_task(parse_news_detail(session, 'https://www.igromania.ru' + link))
                tasks.append(task)

            try:
                results = await asyncio.gather(*tasks)
                return results
            except Exception as e:
                print('An error occurred during gather:', e)
                for task in tasks:
                    if not task.done():
                        task.cancel()


async def parse_news_detail(session, url):
    """
    Парсим детальную страницу новости и возвращаем словарь с данными.
    :param session: aiohttp.ClientSession
    :param url: URL новости
    :return: Словарь с данными новости
    """
    async with session.get(url, headers=HEADERS) as response:
        html = await response.text()
        soup = BS(html, 'html.parser')

        all_elements = soup.find_all('div', {'class': 'TextContent_text__BydqR'})
        image = soup.find(
            'figure',
            {'class': 'MaterialCommonImage_image__GyFHp material-common-image MaterialCommonImage_withCaption__wt5H2'},
        )
        img_element = image.find('img').get('src') if image else ' '

    for element in all_elements:
        news_text = element.text

        query = {'title': news_text}
        update = {
            '$set': {
                'news_text': news_text,
                'link': url,
                'image_link': img_element,
            }
        }
        await collection_igromania.update_one(query, update, upsert=True)
