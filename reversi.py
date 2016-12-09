import os
import pickle
import sys
from contextlib import contextmanager

from PyQt5.QtCore import QBasicTimer, QThread, QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QImage, QIcon, QPixmap, QColor, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget,
                             QMessageBox, QAction)

import argparser
import settings as s
from game.game import Game


class ReversiWindow(QMainWindow):
    def __init__(self, board_size, game_mode, game_difficulty_level,
                 game_time_for_move):
        super().__init__()
        self.images = {}
        self.init_ui(board_size, game_mode, game_difficulty_level,
                     game_time_for_move)

    def init_ui(self, board_size, game_mode, game_difficulty_level,
                game_time_for_move):
        self.game = Game(board_size, mode=game_mode,
                         difficulty_level=game_difficulty_level,
                         is_console_game=False,
                         time_for_move=game_time_for_move)
        self.game_was_saved = False
        self.time_for_move = game_time_for_move
        self.count = self.time_for_move
        self.timer = QBasicTimer()
        self.move_timer = QTimer()
        self.ai_thread = AIThread(self)
        self.ai_thread.finished.connect(self.ai_finish)
        self.ai_finished = True
        self.load_images()
        self.add_toolbar()
        self.font_size = 10
        self.resize(board_size * s.IMG_SIZE,
                    (board_size * s.IMG_SIZE + self.toolbar.height() + 10 +
                     self.font_size))
        self.center()
        self.setWindowTitle('Reversi')
        self.show()
        self.timer.start(1, self)
        self.move_timer.timeout.connect(self.count_down)
        self.move_timer.start(1000)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def add_toolbar(self):
        self.toolbar = self.addToolBar('')
        self.add_toolbar_action(self.toolbar, 'Save', 'save.png', self.save,
                                'Ctrl+S')
        self.add_toolbar_action(self.toolbar, 'Undo', 'undo.png', self.undo,
                                'Ctrl+Z')
        self.add_toolbar_action(self.toolbar, 'Redo', 'redo.png', self.redo)
        self.toolbar.setMovable(False)

    def add_toolbar_action(self, toolbar, name, image, function,
                           shortcut=None):
        action = QAction(QIcon(QPixmap(self.images[image])), name, self)
        if shortcut is not None:
            action.setShortcut(shortcut)
        action.triggered.connect(function)
        toolbar.addAction(action)

    def save(self):
        if self.game.game_state == Game.States.human:
            with open('saved_game.pickle', 'wb') as f:
                pickle.dump(self.game, f, protocol=pickle.HIGHEST_PROTOCOL)
            self.game_was_saved = True

    def undo(self):
        if self.game.game_state == Game.States.human:
            self.reset_count()
            self.game.undo()

    def redo(self):
        if self.game.game_state == Game.States.human:
            self.reset_count()
            self.game.redo()

    def draw_cell(self, painter, cell):
        if cell.state == s.BLACK:
            image = self.images['black.png']
        elif cell.state == s.WHITE:
            image = self.images['white.png']
        elif (cell.get_coordinates() in self.game.mover.next_possible_moves
              and self.game.game_state != Game.States.ai):
            image = self.images['possible_move.png']
        else:
            image = self.images['empty.png']
        painter.drawImage(cell.y*s.IMG_SIZE,
                          (cell.x*s.IMG_SIZE + self.toolbar.height()
                           + self.font_size),
                          image)

    def draw_text(self, painter, font_size):
        painter.setPen(QColor(Qt.black))
        painter.setFont(QFont('Decorative', font_size))
        painter.drawText(QPoint(10, self.toolbar.height() + font_size),
                         'Time left for move: {}'.format(self.count))

    def reset_count(self):
            if not self.ai_thread.isRunning():
                self.count = self.time_for_move

    def count_down(self):
        if self.count != 0:
            self.count -= 1
        else:
            if not self.ai_thread.isRunning():
                self.game.pass_move()
                self.reset_count()
                self.update()

    def ai_finish(self):
        self.update()
        self.reset_count()
        self.ai_finished = True

    def load_images(self):
        images_path = os.path.join(os.getcwd(), 'images')
        for image in os.listdir(images_path):
            self.images[image] = QImage(os.path.join(images_path, image))

    def mousePressEvent(self, QMouseEvent):
        if self.game.game_state == Game.States.human:
            position = QMouseEvent.pos()
            position.setY((position.y() - self.toolbar.height()
                           - self.font_size))
            self.game.next_move(position)
            if self.game.game_state == Game.States.ai:
                self.reset_count()
            self.update()

    def timerEvent(self, event):
        if self.game.is_over():
            self.timer.stop()
            self.move_timer.stop()
            self.show_end_of_game_dialog()
        else:
            if self.game.game_state == Game.States.ai and self.ai_finished:
                self.ai_finished = False
                self.ai_thread.start()
        self.update()

    def paintEvent(self, event):
        with painter(self) as p:
            for cell in self.game.mover.board.cells():
                self.draw_cell(p, cell)
            self.draw_text(p, self.font_size)

    def show_end_of_game_dialog(self):
        message_box = QMessageBox()
        message_box.setText('The game is over! {}'.format
                            (self.game.get_winner_message()))
        message_box.exec_()
        if self.game_was_saved:
            self.ask_question('Do you want to play from your last saved position?',
                              message_box)
            self.check_answer(message_box.exec_(), self.load_saved_game,
                              self.play_again_action)
        else:
            self.play_again_action()

    def play_again_action(self):
        message_box = QMessageBox()
        message_box.setText('Do you want to play again?')
        self.ask_question('', message_box)
        self.check_answer(message_box.exec_(), self.restart,
                          self.close)

    def restart(self):
        self.game_was_saved = False
        self.game.restart()
        self.timer.start(1, self)
        self.move_timer.start(1000)

    def load_saved_game(self):
        with open('saved_game.pickle', 'rb') as f:
            self.game = pickle.load(f)
            self.timer.start(1, self)

    def ask_question(self, question, message_box):
        message_box.setInformativeText(question)
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    def check_answer(self, clicked_button, yes_action, no_action):
        if clicked_button == QMessageBox.Yes:
            yes_action()
        elif clicked_button == QMessageBox.No:
            no_action()
        self.update()


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
                                   argparser.get_mode(namespace),
                                   argparser.get_difficulty_level(namespace),
                                   namespace.time)
    reversi_window.load_images()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()