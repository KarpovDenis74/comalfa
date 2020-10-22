import os
import sys
import xlrd

os.environ['DJANGO_SETTINGS_MODULE'] = 'comalfa.settings'

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import django
django.setup()

from main.models import MainGoods
from django.conf import settings

MEDIA_URL = settings.MEDIA_ROOT + '//'

class RefreshDiscountGoods(object):

    # good = DiscountGoods
    status = '404'

    def __init__(self, data):
        data = data
        self.file = data.get('file')
        response = self.parse_discount()

    def parse_discount(self):
        xls = self.file
        with xlrd.open_workbook(MEDIA_URL + xls) as wb:
            sh = wb.sheet_by_index(0)
            for rownum in range(sh.nrows):
                row = sh.row_values(rownum)
                if(rownum < 8):
                    continue
                item = {
                    'name':str(row[0]),
                    'mark':str(row[1]).replace('-', '.').upper().replace('\\', '/'),
                    'status':'',
                    'type':str(row[6]),
                    'using':str(row[5]),
                    'material':str(row[14]),
                    'analog':str(row[15]),
                    'catalogs':str(row[23]),
                    'weight':str(row[16]),
                    'length':str(row[17]),
                    'using':str(row[18]),
                    'quantity_pack':str(row[19]),
                    'manufactur':str(row[20]),
                    'package':str(row[21]),
                    'note':str(row[22]),
                    'quantity': str(row[3]),
                    'price':str(row[9]),
                    'discount':str(row[10]),
                    'cost':str(row[11]),
                }
                if(item['mark'] == ''):
                    continue
                for mark_item in item['mark'].split('/'):
                    item_mark = str(mark_item).strip()
                    m, created = MainGoods.objects.get_or_create(mark=item_mark)
                    item['mark'] = item_mark
                    item['quantity'] = str(int(float(item['quantity'])))
                    if(item_mark == ''):
                        continue
                    if(row[13] == 'готов'):
                        item['status'] = 'Готов'
                        
                    if(row[13] == 'в перспективе'):
                        item['status'] = 'В перспективе'
                    
                    if(row[13] == 'удален'):
                        item['status'] = 'Удалено'
                    
                    if(row[13] == ''):
                        item['status'] = ''

                    if created:
                        MainGoods.objects.filter(id=m.id).update(**item)
                    else:
                        MainGoods.objects.filter(id=m.id).update(**item)