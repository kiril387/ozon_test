import re
from typing import Optional, List
import requests


def get_hero_list(url: str) -> List[dict]:
    '''
    Возвращает json со всеми героями
    :param url: Юрл адрес API
    :return: Информация о героях в формате JSON
    '''
    try:
        response = requests.get(url=url)
        if response.status_code != 200:
            raise ConnectionError("Ошибка при запросе к API")
        return response.json()
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Ошибка при запросе к API")
    except ValueError:
        raise ValueError("Ошибка при декодировании ответа в JSON")

def filter_heroes(heroes: List[dict], gender: str, has_work:bool) -> List[dict]:
    '''
    Фильтрует список героев по заданным параметрам
    :param heroes: Список героев
    :param gender: Пол супер героя ('Male' или 'Female')
    :param has_work: Наличие работы (True или False)
    :return: Список от фильтрованных героев
    '''
    return [
        hero for hero in heroes
        if hero.get('appearance', {}).get('gender') == gender.capitalize() and
           (hero.get('work', {}).get('occupation') != '-') == has_work
    ]

def get_height(hero: dict) -> float:
    '''
    Возвращает рост в дюймах в формате float
    :param hero: Информация о герое
    :return: Рост героя в дюймах в форме float
    '''
    height = hero.get('appearance', {}).get('height')[0].replace("'", '.')
    try:
        return float(re.search(r"^\d+(\.\d+)?(?<!\.)$", height).string)
    except(ValueError, TypeError, AttributeError):
        return 0.0

def get_tallest_superhero(gender: str = None, has_work: bool = None) -> Optional[dict]:
    '''
    Возвращает самого выского супергероя
    :param gender: Пол супер героя ('Male' или 'Female')
    :param has_work: Наличие работы (True или False)
    :return: Информацию о герое
    '''

    if gender is None or gender.capitalize() not in ('Male', 'Female'):
        raise ValueError("В переменную gender передано значение, которое не равняется одному из Male / Female")
    if not isinstance(has_work, bool):
        raise ValueError("В переменную has_work передано значение, которое не равняется одному из True / False")

    url = 'https://akabab.github.io/superhero-api/api/all.json'
    all_hero_information = get_hero_list(url)

    if len(all_hero_information) == 0:
        raise Exception("Список супергероев пуст")

    filtered_hero_list = filter_heroes(all_hero_information, gender, has_work)

    if len(filtered_hero_list) == 0:
        raise ValueError('Не найдено героев по заданным критериям')

    max_length_hero = max(filtered_hero_list, key=get_height)

    return max_length_hero


if __name__ == "__main__":
    print(get_tallest_superhero("Female", True))
    print(get_tallest_superhero("Male", True))
    print(get_tallest_superhero("FeMaLe", False))
    print(get_tallest_superhero("male", False))
