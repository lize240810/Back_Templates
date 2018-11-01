function send_request(url, action, total, left, origin_text, $btn) {
    var _id = left.shift();
    $.ajax({
        url: url,
        data: {
            action: action,
            id: _id
        },
        dataType: 'json',
        type: 'POST',
        success: function(data) {
            var new_text = '进度: ' + (total - left.length) + '/' + total;
            $btn.attr('value', new_text);
            if(data.error != 0) {
                if(!confirm('Error: ' + data.desc + '\n是否跳过，继续操作?')) {
                    return;
                }
            }
            if(left.length > 0) {
                send_request(url, action, total, left, origin_text, $btn);
            }
            else {
                $btn.attr('value', origin_text);
                setTimeout(function() {
                    $('#tb-staffs').bootstrapTable('refresh', {silent: false});
                }, 50);
            }
        }
    })
}

function delete_or_disable($self, msg, action) {
    if(confirm(msg)) {
        var origin_text = $self.attr('value');
        var ids = get_selected_ids();
        var new_text = '进度: 0/' + ids.length;
        $self.attr('value', new_text);
        send_request(STAFF_DELETE_DISABLE_URL, action, ids.length, ids, origin_text, $self);
    }
}

function get_selected_ids() {
    var $tb_obj = $('#tb-staffs');
    var selection = $tb_obj.bootstrapTable('getSelections');
    var ids = [];
    for (var i = 0; i < selection.length; i++) {
        ids.push(selection[i].id);
    }
    return ids;
}

/**
 * 按钮事件绑定
 */
function bind_click4btns() {
    var $btn_add = $('#btn-add'),
        $btn_disable = $('#btn-disable'),
        $btn_delete = $('#btn-delete');
    $btn_add.on('click', function() {
        popup_staff('添加员工');
    });
    $btn_disable.on('click', function() {
        delete_or_disable($btn_disable, '确定禁用所选的员工吗？', 'disable');
    });
    $btn_delete.on('click', function() {
        delete_or_disable($btn_delete, '确定删除所选的员工吗？', 'delete');
    });
}

/**
 * 改变按钮状态
 * @param  {jQuery对象} $tb_obj 表格对象
 */
function change_enable($tb_obj) {
    var $btn_disable = $('#btn-disable'),
        $btn_delete = $('#btn-delete');
    var selection = $tb_obj.bootstrapTable('getSelections');
    if(selection.length > 0) {
        $btn_disable.removeAttr('disabled').prop('disabled', false);
        $btn_delete.removeAttr('disabled').prop('disabled', false);
    }
    else {
        $btn_disable.attr('disabled', 'disabled').prop('disabled', true);
        $btn_delete.attr('disabled', 'disabled').prop('disabled', true);
    }
}

function build_is_admin(is_admin_val) {
    return [
        '<label>',
            '<input type="radio" name="rdo-is-admin" value="1" ', (is_admin_val == '1' ? 'checked="checked"' : ''), ' />是',
        '</label>',
        '&nbsp;&nbsp;',
        '<label>',
            '<input type="radio" name="rdo-is-admin" value="0" ', (is_admin_val == '0' ? 'checked="checked"' : ''), ' />否',
        '</label>',
    ].join('');
}

function build_is_disable(is_disable_val) {
    return [
        '<label>',
            '<input type="radio" name="rdo-is-disable" value="1" ', (is_disable_val == '1' ? 'checked="checked"' : ''), ' />是',
        '</label>',
        '&nbsp;&nbsp;',
        '<label>',
            '<input type="radio" name="rdo-is-disable" value="0" ', (is_disable_val == '0' ? 'checked="checked"' : ''), ' />否',
        '</label>',
    ].join('');
}

/**
 * 弹出员工信息编辑对话框
 * @param  {String} box_title 对话框标题
 * @param  {Object} staff_item 员工信息
 */
function popup_staff(box_title, staff_item) {
    var is_new = false;
    if(!staff_item) {
        is_new = true;
        staff_item = {
            name: '',
            is_admin: 0,
            email: '',
            advertising: '',
            is_hot: 0,
            pic_url_0: '',
            pic_url_1: '',
            pic_url_2: '',
            pic_url_3: ''
        };
    }
    // console.log(staff_item);
    var htmls = [
        '<div class="box-form-wrapper">'
    ];
    if(!is_new) {
        htmls.push(build_line(
            'ID',
            '<span>' + staff_item.id + '</span>'
        ));
    }
    htmls.push(build_line(
        '姓名',
        '<input type="text" name="txt-name" value="' + staff_item.name + '" placeholder="姓名" />'
    ));
    htmls.push(build_line(
        '邮箱',
        '<input type="text" name="txt-email" value="' + staff_item.email + '" placeholder="邮箱" />'
    ));
    htmls.push(build_line(
        '密码',
        '<input type="text" name="txt-password" value="" placeholder="' + (is_new ? '密码' : '不修改请留空') + '" />'
    ));
    htmls.push(build_line(
        '管理员',
        build_is_admin(staff_item.is_admin)
    ));
    if(!is_new) {
        htmls.push(build_line(
            '禁用',
            build_is_disable(staff_item.disable)
        ));
    }
    htmls.push('</div>');
    htmls.push([
        '<div class="popup-tip-msg">',
            '注意: 操作完成后，请手动点击 [提交] 按钮',
        '</div>'
    ].join(''));
    // http://bootboxjs.com/documentation.html
    bootbox.setLocale('zh_CN');
    var dialog = bootbox.dialog({
        title: box_title,
        message: htmls.join(''),
        show: true,
        backdrop: undefined,
        closeButton: true,
        onEscape: false,
        // size: 'large',
        className: "my-modal",
        buttons: {
            submit: {
                label: '提交',
                className: 'btn-primary',
                callback: function() {
                    console.log(staff_item);
                    var _data = collect_submit_info(dialog, staff_item);
                    if(!!_data) {
                        submit_staff_request(_data);
                        return true;
                    }
                    console.log(_data)
                    return false;
                }
            },
            close: {
                label: '取消',
                className: 'btn-primary',
                callback: function() {
                    return true;
                }
            }
        },
        callback: function(result) {
            return true;
        }
    });
}

function get_staff_by_id(d_id) {
    var ret = null;
    var dl = $('#tb-staffs').data('bootstrap.table').data;
    for (var i = 0; i < dl.length; i++) {
        if(dl[i].id == d_id) {
            ret = dl[i];
            break;
        }
    }
    return ret;
}

function staff_detail(staff_id) {
    if(staff_id) {
        var staff_item = get_staff_by_id(staff_id);
        popup_staff('员工详情', staff_item);
    }
}

/**
 * 提交员工信息
 * @param  {Object} staff_data 员工信息
 */
function submit_staff_request(staff_data) {
    $.ajax({
        url: STAFF_SAVE_AJAX,
        type: 'POST',
        data: {
            staff_data: JSON.stringify(staff_data)
        },
        dataType: 'json'
    }).done(function(data) {
        console.log(data);
        if(data.error == 0) {
            $('#tb-staffs').bootstrapTable('refresh');
        }
        else {
            alert(data.desc);
        }
    }).fail(function(e) {
        console.error(e);
        alert(e.responseText)
    });
}

function collect_submit_info($dialog, staff_item) {
    var $form = $dialog.find('.bootbox-body .box-form-wrapper');
    var is_new = true;
    var _ret = {};
    if(!!staff_item.id) {
        is_new = false;
        _ret['id'] = staff_item.id;
    }
    var _name = $form.find('input[name="txt-name"]').val();
    if(!_name || _name.length < 1) {
        alert('[姓名]必填');
        return null;
    }
    _ret['name'] = _name;
    var _email = $form.find('input[name="txt-email"]').val();
    if(!_email || _email.length < 1) {
        alert('[邮箱]必填');
        return null;
    }
    _ret['email'] = _email;
    var _is_admin = $form.find('input[name="rdo-is-admin"]:checked').val();
    _ret['is_admin'] = _is_admin;
    if(!is_new) {
        var _disable = $form.find('input[name="rdo-is-disable"]:checked').val();
        _ret['disable'] = _disable;
    }
    var _password = $form.find('input[name="txt-password"]').val();
    if(_password && _password.length > 0) {
        _ret['password'] = _password;
    }

    return _ret;
}