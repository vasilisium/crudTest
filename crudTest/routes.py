from flask import request, flash, jsonify, redirect, url_for, Response
from flask import render_template, render_template_string

import os
from crudTest import app, mongo
from crudTest.froms import PostForm, FilterForm
from crudTest.data import getTable, getRecodr, insert_update, getQeryConditions, deleteRecord
from config import Config

def getRequestParametr(request, key):
    param = None
    if key in request.args:
        param = request.args[key]
        try:
            param = int(param)
        except Exception:
            pass
    return param


@app.route('/')
def index():
    mongoCondition = {}
    mongoCondition = getQeryConditions(request)
    if 'id' in mongoCondition:
        del mongoCondition['id']

    tableData = getTable(mongoCondition, request=request)

    responseContext = {
        'form': PostForm(),
        'filterForm': FilterForm(),
        'table': tableData['template'], }
        
    if (tableData['paginator'].limit != getRequestParametr(request,'limit')) or \
    (tableData['paginator'].skip != getRequestParametr(request,'skip')):
        redirectContext = {'limit': tableData['paginator'].limit, 'skip': tableData['paginator'].skip}
        return redirect(url_for('index', **redirectContext))

    resp = Response(render_template('index.html', **responseContext))
    resp.set_cookie(Config.tablePagitation['limit']['key'], str(tableData['paginator'].limit))
    return resp

@app.route('/id/<id>')
def record(id):
    rec = getRecodr(id)
    return rec

@app.route('/iu', methods=['POST']) #input-update form back end
def insertUpdate():
    form = PostForm()
    errors = form.getErrors()
    if errors == {}:
        result = insert_update(form.getData())
        return jsonify({'result': result})
    return jsonify(errors)

@app.route('/filter', methods=['POST'])
def filter():
    ff=FilterForm()
    mongoCondition=ff.getFilterConditions()
    if len(mongoCondition) > 0:
        return getTable(mongoCondition)['template']
    else:
        return getTable()['template']

@app.route('/delete/<id>')
def delete(id):
    result = deleteRecord(id)
    #{'n': 1, 'ok': 1.0}
    n = 0
    if 'ok' in result:
        n = result['n']
        flash(f'Кількість: {n} запис(ів)', category='recordsDeleted')
        return jsonify({'ok': n})
    else:
        return jsonify({})

@app.route('/s')
def scan():
    result = os.system('c:/scanner/tryTwain.exe -s')
    return str(result)