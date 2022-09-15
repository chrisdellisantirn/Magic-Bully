from magic_bully import get_lucky, count_sort, get_api
import pytest

def main():
    test_get_api()
    test_get_lucky()
    test_count_sort()

def test_get_api():
    with pytest.raises(SystemExit) as error:
        get_api('www.badurl.com')
    assert error.value.args[0] == 'Failed to retrieve API'

def test_count_sort():
    assert count_sort([1],[5]) == ([(1, 1)], [(5, 1)])
    assert count_sort([1,2],[5,5]) == ([(1, 1), (2, 1)], [(5, 2)])
    assert count_sort([1,2,2,2,4,4],[5,5,5]) == ([(2, 3), (4, 2), (1, 1)], [(5, 3)])

def test_get_lucky(monkeypatch):
    white_input = iter(['y', 'white', '45'])
    monkeypatch.setattr('builtins.input', lambda _: next(white_input))
    white = get_lucky()
    assert white == ('white', 45)

if __name__ == '__main__':
    main()