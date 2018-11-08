from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

import json
from datetime import datetime

class MyForm(FlaskForm):

    def getErrors(self):
        isValid = FlaskForm.validate(self)
        data = {}
        if not isValid:
            for f in self:
                if f.errors:
                    field = {}
                    field['fieldCaption'] = f.label.text
                    field['errors'] = f.errors
                    data[f.name] = field
        return data

    def getData(self):
        if not FlaskForm.validate(self):
            return None
        data = {}
        for f in self:
            if f.name != 'csrf_token':
                if f.data != '':
                    data[f.name] = f.data
        return data

class PostForm(MyForm):
    name = StringField("Ім`я", [validators.DataRequired(message='Обов\'язкове заповнення'), 
        validators.Length(min=4, max=25, message='Довжина тексту - більша 3, меньша 25')])
    text = StringField("Текст", [validators.DataRequired(message='Обов\'язкове заповнення'), 
        validators.Length(min=4, message='Довжина тексту - більша 3')])
    id = HiddenField()

class FilterForm(MyForm):
    name = StringField('Ім`я')
    text = StringField('Текст')
    date = StringField("Дата")

    def getFilterConditions(self):
        data = super().getData()
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