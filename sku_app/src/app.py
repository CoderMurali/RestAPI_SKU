# -*- coding: utf-8 -*-
"""
Created on Sat Jun 05 10:06:23 2021

@author: muraikv
"""
from flask import Flask,jsonify, current_app
from flask_restx import Api, Resource
import sys

from src.blueprints.bpsku import SKU_BP
# from src.blueprints.bpsku_resource import res_sku_bp

app = Flask(__name__)
api = Api(app)
app.register_blueprint(SKU_BP)
# api.add_resource(res_sku_bp, '/api/sku_api')


