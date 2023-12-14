import pymysql
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QLineEdit, QMenu

from UpdateItemModel import UpdateItemModel
from Utils import Utils
from sqlManger_ui import Ui_MainWindow


# SqlQueryMoedl和QSqlQuery联合使用;
class Manger(QMainWindow):
    def __init__(self, parent=None):
        super(Manger, self).__init__(parent)
        Utils.set_manger_self(self)
        self.db = None
        # 数据库表面板参数
        self.tab_header = []
        self.tab_primary_key = ''

        # 设置UI界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 密码开启隐私模式
        self.ui.pwd.setEchoMode(QLineEdit.Password)
        # 端口限制 0-65535
        port_validator = QIntValidator()
        port_validator.setRange(0, 65535)
        self.ui.port.setValidator(port_validator)

        # 连接槽函数
        self.ui.connbut.clicked.connect(self.conn_database)
        self.ui.querybut.clicked.connect(self.execute_query)
        self.ui.roolbackbut.clicked.connect(self.rollback_database)
        self.ui.commitbut.clicked.connect(self.commit_database)
        self.ui.database.currentIndexChanged.connect(self.change_database)

        self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView.customContextMenuRequested.connect(self.display_table_menu)

    def conn_database(self):
        try:
            connection = Utils.get_connection(self)
            cursor = connection.cursor()

            sql = "SHOW DATABASES"
            # 加载库结构
            if cursor.execute(sql):
                result = cursor.fetchall()
                self.ui.database.clear()
                for i in result:
                    self.ui.database.addItem(i[0])
            Utils.show_msg(self, "数据库链接成功!")
        except Exception as e:
            Utils.show_msg(self, f"数据库链接异常!{e}")

    def execute_query(self):
        try:
            connection = Utils.get_connection(self)
            cursor = connection.cursor()
            connection.rollback()
            if connection is None:
                Utils.show_msg(self, "请先连接数据库!")
            else:
                query_sql = f"select * from `{self.ui.tablename.currentText()}`"
                query_header_sql = f"select COLUMN_NAME, COLUMN_COMMENT,  COLUMN_KEY,DATA_TYPE from information_schema.columns where table_schema = '{self.ui.database.currentText()}' and table_name = '{self.ui.tablename.currentText()}' ORDER BY  ORDINAL_POSITION"
                if self.ui.tablename.currentText() == "":
                    Utils.show_msg(self, "请选择要查询的表格!")
                else:
                    model = UpdateItemModel()
                    model.dataChanged.connect(self.modify_data)
                    # 加载表头
                    cursor.execute(query_header_sql)
                    self.tab_header = []
                    header = []
                    for col in cursor.fetchall():
                        self.tab_header.append(col)
                        header.append(col[0])
                    model.setHorizontalHeaderLabels(header)

                    # 加载数据
                    cursor.execute(query_sql)
                    result = cursor.fetchall()
                    for index, value in enumerate(result):
                        row = []
                        for colTuple in value:
                            if colTuple is None:
                                colTuple = ""
                            col = QStandardItem(str(colTuple))
                            row.append(col)
                        model.appendRow(row)
                        self.load_progress_bar(((index + 1) / len(result)) * 100)

                    self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                    self.ui.tableView.setSortingEnabled(True)
                    self.ui.tableView.setModel(model)
                    # 开启事务
                    cursor.execute("BEGIN")
        except Exception as e:
            Utils.show_msg(self, f"查询失败:{e}")

    def rollback_database(self):
        Utils.get_connection(self).rollback()
        Utils.show_msg(self, "事务回滚成功!")
        self.execute_query()

    def commit_database(self):
        Utils.get_connection(self).commit()
        Utils.show_msg(self, "事务提交成功!")

    def change_database(self):
        try:
            # 切换数据库
            cur_database = self.ui.database.currentText()
            if cur_database == "":
                Utils.show_msg(self, "请选择数据库!")
                return
            connection = Utils.get_connection(self)
            connection.select_db(cur_database)
            cursor = connection.cursor()

            # 加载表
            self.ui.tablename.clear()
            if cursor.execute(f"show tables"):
                result = cursor.fetchall()
                for i in result:
                    self.ui.tablename.addItem(i[0])
        except Exception as e:
            Utils.show_msg(self, f"切换数据库失败:{e}")

    def load_progress_bar(self, progress):
        self.ui.progressBar.setProperty("value", progress)

    def display_table_menu(self, pos):
        # 获取当前行号
        row_index = None
        for i in self.ui.tableView.selectionModel().selection().indexes():
            row_index = i.row()

        # 创建菜单
        menu = QMenu()
        add_item = menu.addAction('新增行')
        del_item = menu.addAction('删除行')

        # 将坐标转化为相对于屏幕的
        screen_pos = self.ui.tableView.mapToGlobal(pos)
        action = menu.exec(screen_pos)

        if action == add_item:
            row = []
            for colInfo in self.tab_header:
                col = QStandardItem()
                row.append(col)
            self.ui.tableView.model().appendRow(row)
        elif action == del_item:
            if row_index is not None:
                self.delete_data()
                self.ui.tableView.model().removeRow(row_index)

        else:
            return

    def insert_data(self):
        print("插入数据")

    def delete_data(self):
        # 删除数据
        try:
            cursor = Utils.get_cursor()
            del_sql = f"delete from `{self.ui.tablename.currentText()}` where id = {self.ui.tableView.currentIndex().row()}"
            print(del_sql)
            cursor.execute(del_sql)
        except Exception as e:
            Utils.show_msg(self, f"删除失败:{e}")

    def modify_data(self):

        # 修改数据
        try:
            row_data = []
            for i in range(len(self.tab_header)):
                row_data.append(self.ui.tableView.model().item(self.ui.tableView.currentIndex().row(), i).text())

            sql_s_list = Utils.get_sql_and_list(self.tab_header, self.ui.tablename.currentText(), row_data, "edit")

            cursor = Utils.get_cursor()
            print(sql_s_list)
            cursor.execute(sql_s_list[0], sql_s_list[1])
        except Exception as e:
            Utils.show_msg(self, f"修改失败:{e}")
            self.execute_query()
