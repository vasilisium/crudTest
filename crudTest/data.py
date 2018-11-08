from flask import render_template, jsonify

from config import Config
from crudTest import mongo
from datetime import datetime
from bson.objectid import ObjectId
from crudTest.paginator import Paginator

def makeList(arg):
    return list(arg)

def insertRecord(data, collectionName='col'):
    data["date"] = datetime.now()
    id = mongo.db[collectionName].insert_one(data).inserted_id
    ido = ObjectId(id)
    mongo.db[collectionName].update_one({'_id': ido}, {'$set': {'id': ido}})
    return id

def insert_update(data, collectionName='col'):
    if 'id' in data:
        if data['id'] != '':
            query = {'_id': ObjectId(data['id'])}
            del data['id']
            mongo.db.col.update_one(query, {'$set': data})
            return 'updated'
    insertRecord(data)
    return 'inserted'

def getTable(query={}, request=None):
    data = mongo.db.col.find(query)
    count = data.count()

    paginator = Paginator(count, request=request)

    if paginator.skip:
        data = data.skip(paginator.skip)
    if paginator.limit :
        data = data.limit(paginator.limit )

    data = data.sort('date', Config.sortOrder)
    return { 
        'template': render_template('table.html', data=data, paginator=paginator, list=makeList),
        'paginator': paginator
    }

def getRecodr(id, collectionName='col'):
    rec = mongo.db[collectionName].find_one({'id': ObjectId(id)})
    if rec:
        for key in rec:
            if isinstance(rec[key], ObjectId):
                rec[key] = str(rec[key])
        return jsonify(rec)
    return jsonify({})

def getQeryConditions(request):
    data = request.args.copy()
    if len(data) > 0:
        if 'limit' in data:
            del data['limit']
        if 'skip' in data:
            del data['skip']
    if len(data) > 0:
        if 'date' in data:
            date = data['date']
            dates = date.split('-')
            del data['date']
            dateConditions = {
                '$gte': datetime.strptime(dates[0].strip(), '%d.%m.%Y'),
                '$lt': datetime.strptime(dates[1].strip(), '%d.%m.%Y'),
            }

            data['date'] = dateConditions

        textCondidions = ['name', 'text']
        for textCondidion in textCondidions:
            if textCondidion in data:
                piceOfData = data[textCondidion]
                del data[textCondidion]
                contition = {'$regex': piceOfData, '$options':'$i'}
                data[textCondidion] = contition

    return data

def deleteRecord(id, collectionName='col'):
    result = mongo.db[collectionName].remove({'_id': ObjectId(id)}, {'justOne': True})
    return result