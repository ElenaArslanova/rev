import sys, os
from game.game import Game
import settings as s
from contextlib import contextmanager
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget,
                             QMessageBox)
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QBasicTimer


class ReversiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.images = {}
        self.init_ui()


    def init_ui(self):
        self.game = Game(s.SIZE, mode = s.Modes.human_ai,
                         is_console_game=False)
        self.timer = QBasicTimer()
        self.load_images()
        self.resize(s.SIZE * s.IMG_SIZE, s.SIZE * s.IMG_SIZE)
        self.center()
        self.setWindowTitle('Reversi')
        self.show()
        self.timer.start(1, self)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def drawCell(self, cell):
        with painter(self) as p:
            if cell.state == s.BLACK:
                image = self.images['black.png']
            elif cell.state == s.WHITE:
                image = self.images['white.png']
            elif cell.get_coordinates() in self.game.mover.next_possible_moves:
                image = self.images['possible_move.png']
            else:
                image = self.images['empty.png']
            p.drawImage(cell.y*s.IMG_SIZE, cell.x*s.IMG_SIZE, image)


    def load_images(self):
        images_path = os.path.join(os.getcwd(), 'images')
        for image in os.listdir(images_path):
            self.images[image] = QImage(os.path.join(images_path, image))

    def mousePressEvent(self, QMouseEvent):
        if self.game.game_state == s.States.human:
            try:
                self.game.next_move(QMouseEvent.pos())
                self.update()
            except ValueError:
                self.game.repeat_player_move()

    def timerEvent(self, event):
        if self.game.is_over():
            self.timer.stop()
            self.show_end_of_game_dialog()
        else:
            self.game.check_player_pass()
            if self.game.game_state == s.States.ai:
                self.game.next_move()
        self.update()

    def paintEvent(self, event):
        for cell in self.game.mover.board.cells():
            self.drawCell(cell)

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


@contextmanager
def painter(pix):
    painter = QPainter()
    painter.begin(pix)
    yield painter
    painter.end()

def main():
    app = QApplication(sys.argv)
    reversi_window = ReversiWindow()
    reversi_window.load_images()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()