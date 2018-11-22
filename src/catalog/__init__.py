# #! /usr/bin/env python3
# # -*- coding: utf-8 -*-

"""Catalog Project server"""
import os
from flask import Flask
from flask_sslify import SSLify

# Flask application
app = Flask(__name__)
sslify = SSLify(app)
app.secret_key = os.urandom(16)
app.config['SESSION_TYPE'] = 'filesystem'

import src.catalog.views
