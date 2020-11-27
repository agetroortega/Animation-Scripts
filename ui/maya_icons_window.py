"""
Shows a window with all Maya icons and a search bar
"""

from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore, QtWidgets
from maya import OpenMayaUI as OpenMayaUI
from maya import cmds

class MayaIcons(QtWidgets.QDialog):
    __object_name = '__fo_maya_icons_ui__'
    def __init__(self, search_filter="*", icon_size=50, parent=None):
        super(MayaIcons, self).__init__(parent=parent)
        self.setObjectName(self.__object_name)
        self.setWindowTitle('Maya Icons')
        self.search_filter = search_filter
        self.icon_size = icon_size

        self.main_layout = QtWidgets.QVBoxLayout()

        # build UI
        self.search_label = QtWidgets.QLabel("Type and press enter to search..")
        self.search_field = QtWidgets.QLineEdit()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.container_widget = QtWidgets.QWidget()
        self.container_layout = QtWidgets.QGridLayout()
        self.container_widget.setLayout(self.container_layout)
        self.container_layout.setColumnStretch(8, 0)
        self.scroll_area.setWidget(self.container_widget)

        # add widgets
        self.main_layout.addWidget(self.search_label)
        self.main_layout.addWidget(self.search_field)
        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        # initialize UI
        self.populate_icons()

        # connections
        self.search_field.returnPressed.connect(self.update_search)

    def update_search(self):
        search_text = self.search_field.text()
        if search_text == "":
            self.search_filter = "*"
        else:
            self.search_filter = "*{}*".format(search_text)
        self.populate_icons()

    def populate_icons(self):
        self._clear_grid_layout()
        for i in self.maya_icons():
            button = IconButton(i, self.icon_size)
            self.container_layout.addWidget(button)

    def maya_icons(self):
        return cmds.resourceManager(nameFilter=self.search_filter)

    def _clear_grid_layout(self):
        for i in reversed(range(self.container_layout.count())):
            self.container_layout.itemAt(i).widget().deleteLater()

    def run(self):
        # Delete any existing instance of the ui in Maya
        ui_name = "{}toolWorkspaceControl".format(self.__object_name)
        if cmds.window(ui_name, query=True, exists=True):
            cmds.deleteUI(ui_name)
        self.show()


class IconButton(QtWidgets.QToolButton):
    def __init__(self, icon_file, icon_size=50, parent=None):
        super(IconButton, self).__init__(parent=parent)
        self.icon_path = ":/{}".format(icon_file)
        self.icon = QtGui.QIcon(self.icon_path)
        # Config button
        self.setToolTip(self.icon_path)
        self.setAutoRaise(True)
        self.setFixedSize(50, 50)
        # add icon
        self.setIcon(self.icon)
        self.setIconSize(QtCore.QSize(icon_size, icon_size))

        # connect click
        self.clicked.connect(self.print_icon)

    def print_icon(self):
        print(self.icon_path)


def get_maya_window():
    mainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)

ic = MayaIcons(search_filter="*", icon_size=60, parent=get_maya_window())
ic.run()
