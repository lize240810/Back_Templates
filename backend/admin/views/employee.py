# -*- coding: utf-8 -*-
'''员工管理'''
import json

from flask import (
    current_app,
    request,
    abort,
    render_template,
    jsonify,
    session
)

from .. import admin_app
from ..models import Staff, db
from ..secure import login_required, admin_required


@admin_app.route(r'/staff/list', methods=['GET'])
@admin_required
def staff_list():
    '''员工列表'''
    staff_list = Staff.query.all()
    print(staff_list)
    return render_template('admin/employee/list.html', staff_list=staff_list)

@admin_app.route(r'/staff/list', methods=['GET', 'POST'])
@admin_required
def staff_list_ajax():
    _offset = request.values.get('offset', None)
    _limit = request.values.get('limit', None)
    Q = Staff.query.filter_by(deleted=False)
    total = Q.count()
    if not _offset is None and _offset.isdigit():
        _offset = int(_offset)
        Q = Q.offset(_offset)
    if not _limit is None and _limit.isdigit():
        _limit = int(_limit)
        Q = Q.limit(_limit)
    ret_data = []
    for staff_obj in Q.all():
        ret_data.append(staff_obj.to_dict(with_pwd=False))
    ret = {
        'rows': ret_data,
        'total': total,
        'error': 0,
        'desc': 'ok'
    }
    return jsonify(ret)

@admin_app.route(r'/staff/delete-disable', methods=['GET', 'POST'])
@admin_required
def staff_delete_or_disable():
    '''编辑员工信息'''
    action = request.values.get('action', None)
    staff_id = request.values.get('id', None)
    ret = {}
    if action in ['disable', 'delete']:
        if not staff_id is None and staff_id.isdigit():
            staff_id = int(staff_id)
            if session['login_staff']['id'] != staff_id:
                staff_obj = Staff.query.get(staff_id)
                if isinstance(staff_obj, Staff):
                    if action == 'disable':
                        staff_obj.disable = True
                        db.session.commit()
                    elif action == 'delete':
                        staff_obj.deleted = True
                        db.session.commit()
                    ret = {
                        'error': 0,
                        'desc': '操作成功'
                    }
                else:
                    ret = {
                        'error': 4,
                        'desc': '请求的员工不存在'
                    }
            else:
                ret = {
                    'error': 3,
                    'desc': '不能对自己进行权限操作'
                }
        else:
            ret = {
                'error': 2,
                'desc': '缺少参数或参数无效'
            }
    else:
        ret = {
            'error': 1,
            'desc': '参数错误'
        }
    return jsonify(ret)

@admin_app.route(r'/staff/save', methods=['POST'])
@admin_required
def staff_save_ajax():
    staff_data = request.values.get('staff_data', None)
    ret = {}
    if bool(staff_data):
        try:
            json_data = json.loads(staff_data)
            if isinstance(json_data, dict):
                required_fields = ['name', 'email']
                if all(i in json_data for i in required_fields):
                    ok = False
                    error = -1
                    msg = '未知错误'
                    if 'id' in json_data:
                        staff_id = int(json_data['id'])
                        if Staff.query.filter_by(id=staff_id).count() > 0:
                            (ok, error) = update_staff_info(staff_id, json_data)
                            msg = '修改成功' if ok else error
                    else:
                        (ok, error) = add_new_staff(json_data)
                        msg = '添加成功' if ok else error
                    ret = {
                        'error': error,
                        'desc': msg
                    }
                else:
                    ret = {
                        'error': 4,
                        'desc': '数据不完整'
                    }
            else:
                ret = {
                    'error': 3,
                    'desc': '数据无效'
                }
        except json.decoder.JSONDecodeError:
            ret = {
                'error': 21,
                'desc': '数据格式有误'
            }
        except Exception as ex:
            raise ex
            ret = {
                'error': 20,
                'desc': '数据内容或结构有误'
            }
    else:
        ret = {
            'error': 1,
            'desc': '缺少参数'
        }
    return jsonify(ret)

def update_staff_info(staff_id, staff_data):
    staff_obj = Staff.query.get(staff_id)
    if 'name' in staff_data:
        staff_obj.name = staff_data['name']
    if 'email' in staff_data:
        # TODO: email格式校验
        staff_obj.email = staff_data['email']
    if 'password' in staff_data and len(staff_data['password']) > 0:
        staff_obj.password = Staff.encrypt_string(staff_data['password'])

    change_permission = False
    if 'is_admin' in staff_data:
        change_permission = True
        staff_obj.is_admin = True if staff_data['is_admin'] in ['1', 'true'] else False
    if 'disable' in staff_data:
        change_permission = True
        staff_obj.disable = True if staff_data['disable'] in ['1', 'true'] else False
    if change_permission and session['login_staff']['id'] == staff_id:
        db.session.rollback()
        return (False, '不能对自己进行权限操作')
    db.session.commit()
    return (True, None)

def add_new_staff(staff_data):
    staff_obj = Staff()
    if 'name' in staff_data:
        staff_obj.name = staff_data['name']
    if 'email' in staff_data:
        # TODO: email格式校验
        staff_obj.email = staff_data['email']
    if 'password' in staff_data:
        staff_obj.password = Staff.encrypt_string(staff_data['password'])
    if 'is_admin' in staff_data:
        staff_obj.is_admin = True if staff_data['is_admin'] in ['1', 'true'] else False
    db.session.add(staff_obj)
    db.session.commit()
    return (True, None)