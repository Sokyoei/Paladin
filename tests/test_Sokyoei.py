import pytest


class TestSokyoei:
    def test_add(self):
        assert 1 == 2 - 1


if __name__ == "__main__":
    pytest.main(["-s", __file__])
