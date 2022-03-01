import sqlite3
import sys
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget, QApplication
from main_ui import *
from addEditCoffeeForm import *


class Edit(QWidget, Ui_Form):
    def __init__(self, conn, parent, id=None):
        super().__init__()
        self.setupUi(self)
        self.id = id
        self.parent = parent
        self.pushButton.clicked.connect(self.submit)
        self.connection = conn

    def submit(self):
        if self.id is None:
            self.connection.cursor().execute(
                '''INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (None,
                 self.sort.text(),
                 self.prozh.text(),
                 self.sost.text(),
                 self.vkus.text(),
                 self.cost.text(),
                 self.value.text())
            )
        else:
            self.connection.cursor().execute(
                '''UPDATE coffee SET id = ?,
                 sort_name = ?, degree_of_roasting = ?, ground_beans = ?, taste_description = ?,
                  cost = ?, packing_volume = ? WHERE id = ?''',
                (self.id,
                 self.sort.text(),
                 self.prozh.text(),
                 self.sost.text(),
                 self.vkus.text(),
                 self.cost.text(),
                 self.value.text(),
                 self.id)
            )
        self.connection.commit()
        self.parent.get_table()
        self.close()


class Application(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = sqlite3.connect("coffee.sqlite")
        self.pushButton.clicked.connect(self.add_data)
        self.pushButton_2.clicked.connect(self.edit_data)
        self.pushButton_2.setEnabled(False)
        self.tableWidget.itemSelectionChanged.connect(self.on_selection)
        self.form = None
        self.get_table()

    def get_table(self):
        data = self.conn.cursor().execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень прожарки", "Молотый/в зернах",
                                                    "Описание вкуса", "Цена", "Объём упаковки"])
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(row[-1])))

    def on_selection(self):
        item = self.tableWidget.selectedItems()
        if item:
            self.tableWidget.selectRow(item[0].row())
            self.pushButton_2.setEnabled(True)
        else:
            self.pushButton_2.setEnabled(False)

    def add_data(self):
        self.form = Edit(self.conn, self)
        self.form.setWindowTitle("Add")
        self.form.show()

    def edit_data(self):
        print(self.tableWidget.currentRow() + 1)
        self.form = Edit(self.conn, self, id=self.tableWidget.currentRow() + 1)
        self.form.setWindowTitle("Edit")
        self.form.show()

    def closeEvent(self, event):
        self.conn.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
