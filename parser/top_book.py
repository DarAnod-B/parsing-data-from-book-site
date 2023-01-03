from enum import Enum
import requests
from selectolax.lexbor import LexborHTMLParser
import os


class Link(Enum):
    url_best_book = r"https://fantlab.ru/rating/work/best?all=1&type=1&threshold=50"
    url_popular_book = r"https://fantlab.ru/rating/work/popular?all=1&type=1&threshold=50"
    url_titled_book = r"https://fantlab.ru/rating/work/titled?all=1&type=1"


class SecretData(Enum):
    login = os.environ.get('_fantlab_login')
    password = os.environ.get('_fantlab_password')


def get_html(url: str) -> str:
    with requests.Session() as session:
        payload = {'login': SecretData.login.value,
                   'password': SecretData.password.value}
        login_url = r"https://fantlab.ru/login"

        session.post(login_url, data=payload)
        result = session.get(url)
        html = result.text
        return html


def text_from_html(html: str) -> list:
    tree = LexborHTMLParser(html)
    tree_url = tree.css(
        "body > div.layout > div > div > div.main-container > main > table:nth-child(6) > tbody"
    )

    check = []
    # Большинство книг, в которых отсутствует данный элемент, не имеют жанровой классификации.
    if tree_url is not None:
        for a in tree_url[0].css("a"):
            check.append(a.attrs['href'][5:])
        return check


def main() -> None:
    with open(r'top_link.txt', 'w', encoding="utf-8") as f:
        f.write(
            str(
                set(
                    text_from_html(get_html(Link.url_best_book.value)) +
                    text_from_html(get_html(Link.url_popular_book.value)) +
                    text_from_html(get_html(Link.url_titled_book.value)))))


if __name__ == "__main__":
    main()
