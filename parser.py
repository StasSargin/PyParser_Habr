import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://habr.com/ru/hub/it_testing/'
FILE = "articles.csv"

# Получаем html.
def get_html(url):
    r = requests.get(url)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_="toggle-menu__item-link_pagination")
    if pagination:
        # Возвращаем количество страниц минус 1, так как последняя это ">|"
        return int(len(pagination)) - 1
    else:
        return 1


# Получаем контент страницы.
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Ищем нужный элемент.
    items = soup.find_all('a', class_="post__title_link")
    # Создаем спискок и сохраняем в него.
    articles = []
    for item in items:
        articles.append({
            'title': item.get_text(),
            'link': item.get('href')
        })
    return articles


# Записываем в файл.
def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Сылка'])
        for item in items:
            writer.writerow([item['title'], item['link']])


# Парсим.
def main():
    html = get_html(URL)
    if html.status_code == 200:
        final_articles = []
        page_count = get_pages_count(html.text)
        for page in range(0, page_count + 1):
            if page == 0:
                html = get_html(URL)
                final_articles.extend(get_content(html.text))
                save_file(final_articles, FILE)
            # Добавляем номер страницы к URL
            else:
                html = get_html(URL + f'page{page_count}')
                final_articles.extend(get_content(html.text))
        print(final_articles)
        print(len(final_articles))
    else:
        print('error')


if __name__ == '__main__':
    main()
