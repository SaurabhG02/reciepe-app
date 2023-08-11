"""
Django cmd to wait fordb to be avl.
"""
import time
from psycopg2 import OperationalError  # noqa
from typing import Any, Optional  # noqa
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Waiting for databse')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except Exception as err:
                print(err)
                self.stdout.write('Database unavlble, waiting 1 sec')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Databse avlbe'))