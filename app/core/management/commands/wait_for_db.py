"""
Django command to wait for the database to be available
"""
from django.core.management.base import BaseCommand
import time
from MySQLdb._exceptions import OperationalError as MySqlError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=["default"])
                db_up = True
            except (MySqlError, OperationalError) as e:
                self.stdout.write("Database Unavailable, waiting for 1 second")
                print(str(e))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available"))