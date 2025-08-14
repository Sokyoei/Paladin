import unittest


class TestAhri(unittest.TestCase):
    def test_add(self):
        self.assertIs(True, True)
        self.assertEqual(12, 6 + 6)


if __name__ == "__main__":
    unittest.main()
