#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from src.catalog.database import (
    database_setup, fakeItems
)

print("Create Catalog Web App Database")
database_setup.setup()
print("Laveraging Random Data into database")
fakeItems.init()
