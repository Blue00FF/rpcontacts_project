# -*- coding: utf-8 -*-
# rpcontacts/model.py

"""This module provides a model to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class contacts_model:
    def __init__(self):
        self.model = self._create_model()

    @staticmethod
    def _create_model():
        """Create and set up the model."""

        table_model = QSqlTableModel()
        table_model.setTable("contacts")

        # Save changes right away
        table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        table_model.select()
        headers = ("ID", "Name", "Job", "Email", "Phone", "Twitter", "Webpage")
        for column_index, header in enumerate(headers):
            table_model.setHeaderData(column_index, Qt.Horizontal, header)
        return table_model

    def add_contact(self, data):
        """Add a contact to the database."""

        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()

    def delete_contact(self, row):
        """Remove a contact from the database."""

        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def clear_all(self):
        """Remove all contacts from the database."""

        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.removeRows(0, self.model.rowCount())
        self.model.submitAll()
        # Reset Edit Strategy to original value.
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()
