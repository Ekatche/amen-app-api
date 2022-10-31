"""
Test custom Django management commands
"""

from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2OpError
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


def test_wait_for_db_ready(patched_check):
    """
    test for database if database ready
    :return:
    """
    patched_check.returned_value = True
    call_command("wait_for_db")
    patched_check.assert_called_once_with(databases=["default"])


@patch("django.db.utils.ConnectionHandler.__getitem__")
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_getitem):
        """Test waiting for database if database ready."""
        patched_getitem.return_value = True

        call_command("wait_for_db")

        self.assertEqual(patched_getitem.call_count, 1)

    @patch("time.sleep")
    def test_wait_for_db_delay(self, patched_sleep, patched_getitem):
        """Test waiting for database when getting OperationalError."""
        patched_getitem.side_effect = (
            [Psycopg2OpError] + [OperationalError] * 5 + [True]
        )

        call_command("wait_for_db")

        self.assertEqual(patched_getitem.call_count, 7)