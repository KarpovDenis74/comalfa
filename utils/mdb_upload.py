 # -*- coding: utf-8 -*-

import os
import glob
import sys
# import pyodbc
import subprocess
import csv

os.environ['DJANGO_SETTINGS_MODULE'] = 'comalfa.settings'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import django
django.setup()

from main.models import Parts, EngineUnits, Engine
from django.conf import settings
from pytils import translit

MEDIA_URL = settings.MEDIA_ROOT + '/'

class UploadMDB(object):

    unit = EngineUnits
    part = Parts

    def __init__(self, data):
        data = data
        self.file = data.get('file')
        self.engine = data.get('engine')
        self.test = data.get('engine')
        self.drivers()


    def getting_related_model(self, field_name):
        related_model = self.part._meta.get_field(field_name).remote_field.model
        return related_model


    def drivers(self):
        mdb = self.file
        MDB = MEDIA_URL + mdb
        USING_TABLES = ['sed', 'det', 'ris']
        CSV_DIR =  os.path.abspath(os.getcwd()) + '/utils/tempcsv/'
        table_names = subprocess.Popen(["mdb-tables", "-1", MDB], 
                               stdout=subprocess.PIPE).communicate()[0]
        tables = table_names.splitlines()

        # Dump each table as a CSV file using "mdb-export",
        # converting " " in table names to "_" for the CSV filenames.
        for table in tables:
            table_name = table.decode("utf-8")
            if (table_name in USING_TABLES):
                filename = table_name.replace(" ","_") + ".csv"
                file = open(CSV_DIR + filename, 'wb')

                contents = subprocess.Popen(["mdb-export", MDB, table_name],
                                            stdout=subprocess.PIPE).communicate()[0]
                
                file.write(contents)
                file.close()

        ALL_UNITS = {}
        ALL_ITEMS = []
        ITEM_MARKS = []
        with open(CSV_DIR + 'ris.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            for row in reader:
                ALL_UNITS[row[0].strip()] = row[3]

        with open(CSV_DIR + 'det.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                item = {
                    'part_unit':'',
                    'id':row[0].strip(),
                    'ris_id':row[1].strip(),
                    'quantity': row[6].strip(),
                    'name': row[4].strip(),
                    'notes': row[7].strip(),
                    'position': row[2].strip(),
                    'marks': '',
                }
                ALL_ITEMS.append(item)

        with open(CSV_DIR + 'sed.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)

            for row in reader:
                mark_item = {
                    'part_id': row[0].strip(),
                    'mark_name': row[4].strip(),
                    'mark_quantity': row[2].strip(),
                    'ass_unit': row[3].strip(),
                }
                ITEM_MARKS.append(mark_item)

        for unit in ALL_UNITS.items():
            for part in ALL_ITEMS:
                if(part['ris_id'] != unit[0]):
                    continue
                related_model = self.getting_related_model('part_unit')
                instance, created = related_model.objects.get_or_create(name=unit[1], engine_name=self.test)
                value = instance
                item = {
                    'part_unit':value,
                    'quantity': part['quantity'],
                    'name': part['name'],
                    'notes': part['notes'],
                    'position': part['position'],
                    'marks': '',
                }
                for mark_item in ITEM_MARKS:
                    if(mark_item['part_id'] != part['id']):
                        continue
                    item['marks'] += mark_item['mark_name'] + ',' + mark_item['ass_unit'] + ',' + str(mark_item['mark_quantity']) + ';'
                m = Parts(**item)
                m.save()

        files = glob.glob(CSV_DIR + '*')
        for f in files:
            os.remove(f)