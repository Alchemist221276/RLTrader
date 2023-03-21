import sys
from MainForm import MainForm
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)

    main_form = MainForm(application=app)
    main_form.show()

    app.exec()


if __name__ == '__main__':
    main()
