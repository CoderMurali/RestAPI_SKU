# -*- coding: utf-8 -*-
"""
Created on Sat Jun 05 10:06:23 2021

@author: muraikv
"""
from flask import Blueprint, jsonify, request
from src.blueprints.model import SkuDB
import json


SKU_BP = Blueprint(name='bpsku', import_name=__name__)
db = SkuDB()


@SKU_BP.route('/api/location', methods=['GET'])
def get_location():
    res = db.fetch_location()
    return jsonify(res)


@SKU_BP.route('/api/location/<location_id>/department', methods=['GET', 'POST'])
def get_sku_by_location(location_id=None):
    res = db.fetch_skus(location_id=location_id)
    return jsonify(res)


@SKU_BP.route('/api/location/<location_id>/department/<dept_id>/category', methods=['GET', 'POST'])
def get_sku_by_loc_dept(location_id=None,dept_id=None):
    res = db.fetch_skus(location_id=location_id, dept_id=dept_id)
    return jsonify(res)


@SKU_BP.route('/api/location/<location_id>/department/<dept_id>/category/<category_id>/subcategory', methods=['GET', 'POST'])
def get_sku_by_loc_dept_category(location_id=None,dept_id=None, category_id=None):
    res = db.fetch_skus(location_id=location_id, dept_id=dept_id, catg_id=category_id)
    return jsonify(res)


@SKU_BP.route('/api/location/<location_id>/department/<dept_id>/category/<category_id>/'
              'subcategory/<sub_category_id>', methods=['GET', 'POST'])
def get_sku_by_loc_dept_category_subcatg(location_id=None,dept_id=None, category_id=None, sub_category_id=None):
    res = db.fetch_skus(location_id=location_id, dept_id=dept_id, catg_id=category_id, sub_catg_id=sub_category_id)
    return jsonify(res)


@SKU_BP.route('/api/sku/<sku_name>/location/<location_id>/department/<dept_id>/category/<category_id>/subcategory'
              '/<sub_category_id>', methods=['POST'])
def ins_sku_data(sku_name=None,location_id=None,dept_id=None, category_id=None, sub_category_id=None):
    sku_ins_data ={
        'sku_name' : sku_name
        , 'location_id' : location_id
        , 'dept_id': dept_id
        , 'catg_id' : category_id
        , 'sub_catg_id' : sub_category_id
    }
    res = db.insert_sku(**sku_ins_data)
    return jsonify(res)


@SKU_BP.route('/api/sku/<sku_name>/location/<location_id>/', methods=['PUT'])
def upd_sku_by_loc(sku_name=None,location_id=None):
    d = request.get_json()
    kwargs = { 'filter': {
        'sku_name': sku_name
        , 'location_id': location_id
    }, 'data': {
        'dept_id': d['dept_id']
        , 'category_id': d['category_id']
        , 'sub_category_id': d['sub_category_id']
    }
    }
    res = db.update_sku(**kwargs)
    return jsonify(res)


@SKU_BP.route('/api/sku/<sku_name>/location/<location_id>/department/{dept_id}/', methods=['PUT'])
def upd_sku_by_loc_dept(sku_name=None,location_id=None, dept_id=None):
    d = request.get_json()

    kwargs = { 'filter' : {
        'sku_name': sku_name
        , 'location_id': location_id
        , 'dept_id': dept_id
    }, 'data': {
        'category_id': d['category_id']
        , 'sub_category_id': d['sub_category_id']
    }
    }
    res = db.update_sku(**kwargs)
    return jsonify(res)


@SKU_BP.route('/api/sku/<sku_name>/location/<location_id>/department/<dept_id>/category/<category_id>/subcategory'
              '/<sub_category_id>', methods=['DELETE'])
def del_sku_data(sku_name=None, location_id=None, dept_id=None, category_id=None, sub_category_id=None):
    sku_del_data = {
        'sku_name': sku_name
        , 'location_id': location_id
        , 'dept_id': dept_id
        , 'catg_id': category_id
        , 'sub_catg_id': sub_category_id
    }
    res = db.delete_sku(**sku_del_data)
    return jsonify(res)
