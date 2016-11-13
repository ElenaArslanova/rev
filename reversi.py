import os
import sys
from contextlib import contextmanager

from PyQt5.QtCore import QBasicTimer, QThread
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget,
                             QMessageBox)

import argparser
import settings as s
from game.game import Game


class ReversiWindow(QMainWindow):
    def __init__(self, board_size, game_mode):
        super().__init__()
        self.images = {}
        self.init_ui(board_size, game_mode)


    def init_ui(self, board_size, game_mode):
        self.game = Game(board_size, mode =game_mode, is_console_game=False)
        self.timer = QBasicTimer()
        self.ai_thread = AIThread(self)
        self.ai_thread.finished.connect(self.update)
        self.load_images()
        self.resize(board_size * s.IMG_SIZE, board_size * s.IMG_SIZE)
        self.center()
        self.setWindowTitle('Reversi')
        self.show()
        self.timer.start(1, self)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def draw_cell(self, painter, cell):
        if cell.state == s.BLACK:
            image = self.images['black.png']
        elif cell.state == s.WHITE:
            image = self.images['white.png']
        elif cell.get_coordinates() in self.game.mover.next_possible_moves:
              # and self.game.game_state != s.States.ai):
            image = self.images['possible_move.png']
        else:
            image = self.images['empty.png']
        painter.drawImage(cell.y*s.IMG_SIZE, cell.x*s.IMG_SIZE, image)


    # def draw_text(self, painter):
    #     painter.setPen(QColor(168, 34, 3))
    #     painter.setFont(QFont('Decorative', 10))
    #     painter.drawText(QPoint(s.SIZE * s.IMG_SIZE + 10, 50), self.game.get_current_player().colour)

    def load_images(self):
        images_path = os.path.join(os.getcwd(), 'images')
        for image in os.listdir(images_path):
            self.images[image] = QImage(os.path.join(images_path, image))

    def mousePressEvent(self, QMouseEvent):
        if self.game.game_state == s.States.human:
            self.game.next_move(QMouseEvent.pos())
            self.update()

    def timerEvent(self, event):
        if self.game.is_over():
            self.timer.stop()
            self.show_end_of_game_dialog()
        else:
            if self.game.game_state == s.States.ai:
                self.ai_thread.start()
        self.update()

    def paintEvent(self, event):
        with painter(self) as p:
            # self.draw_text(p)
            for cell in self.game.mover.board.cells():
                self.draw_cell(p, cell)

    def show_end_of_game_dialog(self):
        message_box = QMessageBox()
        message_box.setText('The game is over! {}'.format
                            (self.game.get_winner_message()))
        message_box.setInformativeText('Do you want to play again?')
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.check_answer(message_box.exec_())

    def check_answer(self, clicked_button):
        if clicked_button == QMessageBox.Yes:
            self.game.restart()
            self.timer.start(1, self)
            self.update()
        elif clicked_button == QMessageBox.No:
            self.close()


class AIThread(QThread):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.game.next_move()


@contextmanager
def painter(pix):
    painter = QPainter()
    painter.begin(pix)
    yield painter
    painter.end()

def main():
    app = QApplication(sys.argv)
    reversi_parser = argparser.create_parser()
    namespace = reversi_parser.parse_args()
    reversi_window = ReversiWindow(namespace.size,
                                   argparser.get_mode(namespace))
    reversi_window.load_images()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()