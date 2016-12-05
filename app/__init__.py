# -*- coding: utf-8 -*-
__author__ = 'wangbb13'

from flask import Flask

app = Flask(__name__)

from app.views import views
app.register_blueprint(views.mod)
