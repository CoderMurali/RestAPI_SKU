# -*- coding: utf-8 -*-
"""
Created on Sat Jun 05 10:06:23 2021

@author: muraikv
"""
from flask import current_app
from src.dbconnect import Database


class SkuDB:
    def __init__(self):
        self.db = Database()
        self.connect = self.db.connect()
        self.dept_filter = ''
        self.catg_filter = ''
        self.sub_catg_filter = ''
        self.where = ''
        self.set_stmt = ''


    def fetch_location(self):
        location_query = 'SELECT location_id, location FROM tbl_location'
        curs = self.db.execute(location_query)
        res = curs.fetchall()
        return res

    def fetch_location_department(self, location_id):
        loc_dept_query = '''
        select l.location, d.department
        from tbl_location l inner join tbl_department d 
        on l.location_id = d.location_id
        where l.location_id = {location_id}
            '''
        query = loc_dept_query.format(location_id=location_id)
        curs = self.db.execute(query)
        res = curs.fetchall()
        return res

    def fetch_skus(self, location_id, dept_id=None, catg_id=None, sub_catg_id=None):
        sku_query = '''
        select
        s.sku_name, l.location, d.department, c.category, sc.sub_category
        from tbl_sku_data s 
        inner join tbl_location l on s.location_id= l.location_id
        left join tbl_department d on s.dept_id = d.dept_id 
        left join tbl_category c on s.category_id = c.category_id 
        left join tbl_sub_category sc on s.sub_category_id = sc.sub_category_id
        where s.location_id = {location_id} 
        '''
        sku_query = sku_query.format(location_id=location_id)
        if dept_id:
            self.dept_filter = ' and s.dept_id = {dept_id}'.format(dept_id=dept_id)
        if catg_id:
            self.catg_filter = ' and s.category_id = {catg_id}'.format(catg_id=catg_id)
        if sub_catg_id:
            self.sub_catg_filter = ' and s.sub_category_id = {sub_catg_id}'.format(sub_catg_id=sub_catg_id)

        sku_query = sku_query + self.dept_filter + self.catg_filter + self.sub_catg_filter

        # print(sku_query)
        curs = self.db.execute(sku_query)
        res = curs.fetchall()
        if res:
            return res
        else:
            message = 'No Matching Sku''s with the location_id :{location_id}'.format(
                location_id=location_id) + ', dept_id :{dept_id}'.format(dept_id=dept_id) if dept_id else ''
            #  + ', category_id: {catg_id}'.format(
            # catg_id=catg_id) if catg_id else '' + 'sub_category_id: {sub_category_id}'.format(
            # sub_category_id=sub_catg_id) if sub_catg_id else ' '
            return message

    def insert_sku(self, **data):
        ins_query = '''
                    Insert into tbl_sku_data(sku_name, location_id, dept_id, category_id, sub_category_id)
                    values(%s, %s , %s, %s, %s)
                    '''
        params = (data['sku_name'], data['location_id'], data['dept_id'], data['catg_id'], data['sub_catg_id'])
        status = self.db.exe_modiy(ins_query, params)
        if isinstance(status, str):
            return 'Failure ! Data failed to insert , Reason: {}'.format(status)
        else:
            return 'Success! Data inserted' if status == 1 else 'Failure ! Data failed to insert'

    def update_sku(self, **kwargs):
        self.where = ''
        self.set_stmt=''
        condition = kwargs['filter']
        data = kwargs['data']
        for k,v in condition.items():
            if self.where:
                self.where = self.where + ''' and {key} = '{val}' '''.format(key=k, val=v)
            else:
                self.where = self.where + ''' where {key} = '{val}' '''.format(key=k, val=v)

        for k,v in data.items():
            if self.set_stmt:
                self.set_stmt = self.set_stmt + ''' , {key} = {val} '''.format(key=k, val=v)
            else:
                self.set_stmt = self.set_stmt + ''' {key} = {val} '''.format(key=k, val=v)

        upd_query = '''
                    update tbl_sku_data
                    set {set_stmt}
                    {where} '''
        upd_query = upd_query.format(set_stmt=self.set_stmt, where=self.where)
        print(upd_query)
        status = self.db.exe_modiy(upd_query, None)
        if isinstance(status, str):
            return 'Failure ! Data failed to update , Reason: {}'.format(status)
        else:
            return 'Success! Data updated' if status == 1 else 'Failure ! Data failed to update'

    def delete_sku(self, **data):
        del_query = '''
                    DELETE FROM tbl_sku_data
                    WHERE sku_name = '{sku_name}'
                    AND  location_id = {location_id}
                    AND  dept_id = {dept_id}
                    AND  category_id = {category_id}
                    AND  sub_category_id = {sub_category_id}
                   '''
        del_query = del_query.format(sku_name=data['sku_name'], location_id=data['location_id'],
                                     dept_id = data['dept_id'],
                                     category_id=data['catg_id'],
                                     sub_category_id=data['sub_catg_id'])
        print(del_query)
        status = self.db.exe_modiy(del_query, params=None)
        if isinstance(status, str):
            return 'Failure ! Data failed to delete , Reason: {}'.format(status)
        else:
            return 'Success! Data delete' if status == 1 else 'Failure ! Data failed to delete'
