# -*- coding: utf-8 -*-

"""This module provides views to manage the contacts table."""

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .model import contacts_model


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initialiser."""
        super().__init__(parent)
        self.setWindowTitle("RP Contacts")
        self.resize(550, 250)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contacts_model = contacts_model()
        self.setup_ui()

    def setup_ui(self):
        """Setup the main window's GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.contacts_model.model)
        # Set the selection behavior property of the table
        # SelectRows means that when clicking on a cell the whole
        # row will be selected.
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()

        # Create the buttons
        self.add_button = QPushButton("Add...")
        self.add_button.clicked.connect(self.open_add_dialog)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_contacts)
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_contacts)

        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addStretch()
        layout.addWidget(self.clear_all_button)

        # Initialise the GUI
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def open_add_dialog(self):
        """Open the Add Contact dialog."""

        dialog = add_dialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contacts_model.add_contact(dialog.data)
            self.table.resizeColumnsToContents()

    def delete_contacts(self):
        """Delete the selected contact from the database."""
        row = self.table.currentIndex().row()
        if row < 0:  # Corresponds to empty database.
            return

        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )

        if message_box == QMessageBox.Ok:
            self.contacts_model.delete_contact(row)

    def clear_contacts(self):
        """Remove all contacts from the database."""

        message_box = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to delete all your contacts?",
            QMessageBox.Ok | QMessageBox.Cancel
        )

        if message_box == QMessageBox.Ok:
            self.contacts_model.clear_all()


class add_dialog(QDialog):
    """Add Contact dialog."""

    def __init__(self, parent=None):
        """Initialiser."""
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the Add Contact dialog's GUI."""

        # Create line edits for data fields.

        self.name_field = QLineEdit()
        self.name_field.setObjectName("Name")
        self.job_field = QLineEdit()
        self.job_field.setObjectName("Job")
        self.email_field = QLineEdit()
        self.email_field.setObjectName("Email")

        # Arrange the line edits in a particular form.
        layout = QFormLayout()
        layout.addRow("Name:", self.name_field)
        layout.addRow("Job:", self.job_field)
        layout.addRow("Email:", self.email_field)
        self.layout.addLayout(layout)

        # Add standard buttons to the dialog and connect them.
        self.buttons_box = QDialogButtonBox(self)
        self.buttons_box.setOrientation(Qt.Horizontal)
        self.buttons_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons_box.accepted.connect(self.accept)
        self.buttons_box.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons_box)

    def accept(self):
        """Accept the data provided through the dialog."""
        # The reject slot is built into the dialog, accept isn't

        self.data = []
        for field in (self.name_field, self.job_field, self.email_field):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}"
                )
                self.data = None
                return

            self.data.append(field.text())

        if not self.data:
            return

        super().accept()
