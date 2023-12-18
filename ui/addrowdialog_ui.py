# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addrowdialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog, form_items=[]):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.form_items = form_items
        self.add_row_but = QtWidgets.QDialogButtonBox(Dialog)
        self.add_row_but.setGeometry(QtCore.QRect(30, 260, 341, 32))
        self.add_row_but.setOrientation(QtCore.Qt.Horizontal)
        self.add_row_but.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.add_row_but.setObjectName("add_row_but")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(20, 10, 361, 241))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 359, 239))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout.setObjectName("formLayout")

        # 动态添加表单
        for i, item in enumerate(form_items):
            column_name = item[0]
            column_comment = item[1]
            column_key = item[2]
            data_type = item[3]
            setattr(self, f"label_{column_name}", QtWidgets.QLabel(self.scrollAreaWidgetContents))
            getattr(self, f"label_{column_name}").setObjectName(f"label_{column_name}")
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, getattr(self, f"label_{column_name}"))
            setattr(self, f"lineEdit_{column_name}", QtWidgets.QLineEdit(self.scrollAreaWidgetContents))
            getattr(self, f"lineEdit_{column_name}").setObjectName(f"lineEdit_{item}")
            getattr(self, f"lineEdit_{column_name}").setPlaceholderText(f"{column_comment}")

            if column_key == 'PRI':
                getattr(self, f"lineEdit_{column_name}").setPlaceholderText(f"主键")
            if data_type == 'int':
                getattr(self, f"lineEdit_{column_name}").setValidator(QtGui.QIntValidator())
            elif data_type == 'float':
                getattr(self, f"lineEdit_{column_name}").setValidator(QtGui.QDoubleValidator())
            elif data_type == 'date':
                getattr(self, f"lineEdit_{column_name}").setInputMask("0000-00-00")
            elif data_type == 'datetime':
                getattr(self, f"lineEdit_{column_name}").setInputMask("0000-00-00 00:00:00")

            self.formLayout.setWidget(i, QtWidgets.QFormLayout.FieldRole, getattr(self, f"lineEdit_{column_name}"))

        # self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        # self.label.setObjectName("label")
        # self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        # self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        # self.lineEdit.setObjectName("lineEdit")
        # self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        # self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        # self.label_2.setObjectName("label_2")
        # self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        # self.lineEdit_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        # self.lineEdit_2.setObjectName("lineEdit_2")
        # self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.retranslateUi(Dialog)
        self.add_row_but.accepted.connect(Dialog.accept)  # type: ignore
        self.add_row_but.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        for i, item in enumerate(self.form_items):
            getattr(self, f"label_{item[0]}").setText(_translate("Dialog", item[0]))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
