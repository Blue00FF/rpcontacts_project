# -*- coding: utf-8 -*-
# rpcontacts/main.py

"""This module provides RP Contacts application."""

import sys

from PyQt5.QtWidgets import QApplication

from .database import create_connection
from .views import Window


def main():
    """RP Contacts main function."""
    # Create the application
    app = QApplication(sys.argv)
    # Attempt connection to the database
    if not create_connection("contacts.sqlite"):
        sys.exit(1)
    # Create the main window if the connection succeeded
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())
