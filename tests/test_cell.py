import kit
from random import randint, choice
import unittest
from settings import *


class TestCell(unittest.TestCase):
    def test_cell(self):
        for i in range(100):
            x = randint(0, 7)
            y = randint(0, 7)
            cell = kit.Cell(x, y)
            self.assertIs(cell.state, EMPTY)
            self.assertEqual(cell.x, x)
            self.assertEqual(cell.y, y)
            colour = choice([WHITE, BLACK])
            if colour == BLACK:
                cell.set_black()
                self.assertIs(cell.state, BLACK)
            else:
                cell.set_white()
                self.assertIs(cell.state, WHITE)
            self.assertIn(cell.get_state(), [EMPTY, WHITE, BLACK])

    def test_flip(self):
        for i in range(100):
            cell = kit.Cell(randint(0, 7), randint(0, 7))
            colour = choice([WHITE, BLACK])
            if colour == WHITE:
                cell.set_white()
                self.assertIs(cell.get_state(), WHITE)
                cell.flip()
                self.assertIs(cell.get_state(), BLACK)
            else:
                cell.set_black()
                self.assertIs(cell.get_state(), BLACK)
                cell.flip()
                self.assertIs(cell.get_state(), WHITE)


if __name__ == '__main__':
    unittest.main()
