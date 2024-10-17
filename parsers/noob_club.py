import aiohttp
from bs4 import BeautifulSoup as BS

from core.mongodb.connecttion import collection
from parsers.settings import HEADERS, URL_NOOB_CLUB


async def parse_noob_club():
    """
    Парсим сайт с новостями noob-club и сохраняем список словеарей в MongoDB.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(URL_NOOB_CLUB, headers=HEADERS) as response:
            html = await response.text()
            soup = BS(html, 'html.parser')

            items = soup.find_all('span', {'class': 'entry-header'})

            for item in items:
                # Находим название новости
                title_element = item.find('a')
                title = title_element.text.strip()

                # Описание новости
                entry_content = item.find_next_sibling('span', {'class': 'entry-content'})
                news_text = entry_content.get_text().strip()

                # Ссылка на новость
                link = title_element['href']
                full_link = URL_NOOB_CLUB + link

                # Находим иконку
                game_icon = item.find('span', {'class': 'game-icon'})
                game_icon_class = game_icon['class'][-1] if game_icon else None

                # Находим картинку новости
                image_tag = entry_content.find_all('img')
                for image_link in image_tag:
                    image_source = image_link.get('src')

                    # Сохраняем данные в MongoDB (с использованием upsert для записи уникальных значений)
                    query = {'title': title}
                    update = {
                        '$set': {
                            'title': title,
                            'news_text': news_text,
                            'link': full_link,
                            'game_icon_class': game_icon_class,
                            'image_link': image_source,
                        }
                    }
                    await collection.update_one(query, update, upsert=True)
