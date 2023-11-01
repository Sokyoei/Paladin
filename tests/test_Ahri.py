import unittest


class TestAhri(unittest.TestCase):
    def test_add(self):
        self.assertIs(True, True)
        self.assertEqual(12, 1 + 1)


if __name__ == "__main__":
    unittest.main()
