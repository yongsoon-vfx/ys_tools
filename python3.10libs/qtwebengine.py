from PySide2 import QtWidgets

from PySide2 import QtWidgets
from PySide2.QtWebEngineWidgets import QWebEngineView


def createInterface():
    # Create a calendar widget and a label.

    browser = QWebEngineView()
    browser.setUrl("https://www.youtube.com/")
    # Create a widget with a vertical box layout.
    # Add the label and calendar to the layout.
    root_widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(browser)

    root_widget.setLayout(layout)

    # Return the top-level widget.
    return root_widget
