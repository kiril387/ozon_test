import pytest
from unittest.mock import patch, Mock
from main import get_tallest_superhero, get_hero_list
from heroes import heroes


@pytest.fixture
def mock_get_hero_list():
    with patch('main.get_hero_list') as mock:
        yield mock

@pytest.fixture
def mock_request():
    with patch('requests.get') as mock:
        yield mock


def test_get_superhero_list_status_code_200(mock_request):
    '''
    Тест функции get_superhero_list
    Цель:
        Проверить, что функция возвращает список героев если status code = 200
    '''
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = heroes
    mock_request.return_value = mock_response
    assert get_hero_list('https://akabab.github.io/superhero-api/api/all.json') == heroes

@pytest.mark.parametrize(
    "status_code", [300, 400, 404, 500]
)
def test_get_superhero_list_status_code_not_200(mock_request, status_code):
    '''
    Тест функции get_superhero_list
    Цель:
        Проверить, что функция вызывает исключение если status code != 200
    '''
    mock_request.return_value.status_code = status_code
    with pytest.raises(ConnectionError, match="Ошибка при запросе к API"):
        get_hero_list('https://akabab.github.io/superhero-api/api/all.json')


@pytest.mark.parametrize(
    "gender, has_work, expected_id, expected_name, expected_height",
    [
        ('Male', True, 1, "A-Bomb", ["6'8", "203 cm"]),
        ('Male', False, 17, "Amazo", ["8'5", "257 cm"]),
        ('Female', True, 20, "Killer Frost", ["5'9", "175 cm"]),
        ('Female', False, 21, "Lady Deathstrike", ["5'9", "175 cm"]),
        ('female', False, 21, "Lady Deathstrike", ["5'9", "175 cm"]),
        ('FEMALE', False, 21, "Lady Deathstrike", ["5'9", "175 cm"]),
    ]
)
def test_get_tallest_superhero(mock_get_hero_list, gender, has_work, expected_id, expected_name, expected_height):
    '''
    Тест функции get_tallest_superhero с параметрами gender и has_work
    Цель:
        Проверить, что функция возвращает самого высокого супергероя
    '''
    mock_get_hero_list.return_value = heroes
    super_hero = get_tallest_superhero(gender, has_work)
    assert super_hero.get('id') == expected_id
    assert super_hero.get('name') == expected_name
    assert super_hero.get('appearance', {}).get("height") == expected_height


@pytest.mark.parametrize(
    "gender, has_work, exception_message",
    [
        ('', True, "В переменную gender передано значение, которое не равняется одному из Male / Female"),
        ('Male1', True, "В переменную gender передано значение, которое не равняется одному из Male / Female"),
        ('Мужчина', True, "В переменную gender передано значение, которое не равняется одному из Male / Female"),
        ('Male!', True, "В переменную gender передано значение, которое не равняется одному из Male / Female"),
    ]
)
def test_get_tallest_superhero_invalid_gender(mock_get_hero_list, gender, has_work, exception_message):
    '''
    Тест функции get_tallest_superhero с недопустимыми значениями gender
    Цель:
        Проверить, что функция вызывает исключение ValueError
    '''
    mock_get_hero_list.return_value = heroes
    with pytest.raises(ValueError, match=exception_message):
        get_tallest_superhero(gender, has_work)


@pytest.mark.parametrize(
    "has_work, exception_message",
    [
        ('', "В переменную has_work передано значение, которое не равняется одному из True / False"),
        ('True', "В переменную has_work передано значение, которое не равняется одному из True / False"),
        (1, "В переменную has_work передано значение, которое не равняется одному из True / False"),
        ('Работает', "В переменную has_work передано значение, которое не равняется одному из True / False"),
        ('True!', "В переменную has_work передано значение, которое не равняется одному из True / False"),
    ]
)
def test_get_tallest_superhero_invalid_has_work(mock_get_hero_list, has_work, exception_message):
    '''
    Тест функции get_tallest_superhero с недопустимыми значениями has_work
    Цель:
        Проверить, что функция вызывает исключения ValueError
    '''
    mock_get_hero_list.return_value = heroes
    with pytest.raises(ValueError, match=exception_message):
        get_tallest_superhero('Male', has_work)


def test_get_tallest_superhero_with_empty_heroes_list(mock_get_hero_list):
    '''
    Тест функции get_tallest_superhero при условии, что возвращается пустой список супергероев
    Цель:
        Проверить, что функция вызывает исключение при пустом списке супергероев с указанным полом и статусом работы
    '''
    mock_get_hero_list.return_value = []
    with pytest.raises(Exception, match="Список супергероев пуст"):
        get_tallest_superhero("Male", True)


def test_get_tallest_superhero_missing_gender_args(mock_get_hero_list):
    '''
    Тест функции get_tallest_superhero с недостающими аргументами
    '''
    mock_get_hero_list.return_value = heroes
    with pytest.raises(ValueError, match="В переменную gender передано значение, которое не равняется одному из Male / Female"):
        get_tallest_superhero(has_work=True)

def test_get_tallest_superhero_missing_has_work_args(mock_get_hero_list):
    '''
    Тест функции get_tallest_superhero с недостающими аргументами
    '''
    mock_get_hero_list.return_value = heroes
    with pytest.raises(ValueError, match="В переменную has_work передано значение, которое не равняется одному из True / False"):
        get_tallest_superhero(gender="Male")
