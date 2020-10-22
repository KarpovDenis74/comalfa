# Реализация модели каталога запчастей для двигателей.
# class Catalog
# Иерархия (не определена изначально):
# Двигатель,
#     у двигателя есть узлы и агрегаты
#         у узлов и агрегатов есть сборные элементы
#             сборные элементы состоят из деталей
#                 детали - конечный элементы
# Например:
# Двигатель
#     узел каленвала и узел коробки передач
#         у узла каленвала есть блок крепления
#         у узла коробки передач есть узел синхронизации
#             на блок крепления нужны гайки М12
#             на узел синхронизации нужны гайки М12

# class Groups
# Каждый элемент каталога относится к какой - то группе
# Например, структура группы:
# Двигатель
#     Узел
#     Агрегат
#         Сборный элемент
#             Деталь
# Деталь (например гайка или шайба) может входить как в узел, так и в Сборный элемент, так и в Агрегат
# Сборный элемент может входить как в один Узел, так и в несколько сразу и т.д.

# class Engine
# Описывает какие двигатели есть 

# class EngineItems
# Описыват сколько и каких частей нужно на двигатель



# Вопрос:
# Детали на складе(гайки, шайбы и т.д.могут быть оригинальные, а могут быть аналоги)
# И те и другие подходят на узел.Их общее количество должно быть count(например: 8) в модели EngineItems
# Если гайки оригинальные закинуть в EngineItems с count = 8
# и не оригинальные закинуть в EngineItems с count = 8, то получается в двигателе нужны и те и те.
# А на самом деле нужны либо оригинальные (8 штук), либо аналог (8 штук), либо(например, 3 оригинальных и 5 аналогов)
# Как реализовать множественность выбора, при этом чтобы общее количество было определенным

from django.db import models
# import string
# import datetime
# from django.shortcuts import render
# from django.http import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files.base import ContentFile
from django.template import RequestContext
# import json
# import PyPDF2
# from pytils import translit
import os
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image

class Groups(model.Model):
    parents = models.ManyToManyField(
        'self', related_name='parents', verbose_name='Относится к')
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Группы товаров'


class Engine(model.Model):
    
    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["Engine_images/", translit.slugify(filename.strip()), '.', ext])
        return path

    def get_filePDF_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["GuidesForEngines/", translit.slugify(filename.strip()), '.', ext])
        return path

    seriesEngine = models.CharField(max_length=200, verbose_name='Название')
    name = models.CharField(max_length=200, verbose_name='Название')
    img = models.ImageField(upload_to=get_image_path,
                            verbose_name='Схема', blank=True, null=True)
    filePDF = models.FileField(storage=fs, upload_to=get_filePDF_path,
                               verbose_name='Документ pdf', blank=True, null=True, default='default_pdf.pdf')
    processed = models.BooleanField(
        default=False, verbose_name='Без пароля и водяного знака')

    def filename(self):
        return os.path.basename(self.filePDF.name)

    class Meta:
        verbose_name = u'Название Двигателя'
        verbose_name_plural = u'Название Двигателей'

    def __str__(self):
        return self.name


class EngineItems(model.Model):
    element = models.ForeignKey(
        Catalog, on_delete=models.CASCADE, verbose_name='Элемент двигателя', blank=False)
    engine = models.ForeignKey(
        Catalog, on_delete=models.CASCADE, verbose_name='Двигатель', blank=False)
    count = models.IntegerField()

    def __str__(self):
        return self.count

    class Meta:
        verbose_name = u'Элемент двигателя'
        verbose_name_plural = u'Элементы двигателя'


class Catalog(model.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["Catalog_images/", translit.slugify(filename.strip()), '.', ext])

    def filename(self):
        return os.path.basename(self.filePDF.name)
    
    def get_filePDF_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["GuidesForEngines/", translit.slugify(filename.strip()), '.', ext])
        return path

    def __str__(self):
        return self.name

    parents = models.ManyToManyField(
        'self', related_name='parents', verbose_name='Относится к')
    group = models.ForeignKey(
        Group, related_name='group', verbose_name='Группа')
    name = models.CharField(max_length=200, verbose_name='Название')
    manufactur = models.CharField(
        max_length=200, verbose_name='Завод производитель', blank=True)
    series = models.CharField(max_length=200, verbose_name='Серия')
    img = models.ImageField(upload_to=get_image_path,
                            verbose_name='Фото', blank=True, null=True)
    filePDF = models.FileField(storage=fs, upload_to=get_filePDF_path,
                               verbose_name='Документ pdf', blank=True,
                               null=True, default='default_pdf.pdf')
    processed = models.BooleanField(
        default=False, verbose_name='Без пароля и водяного знака')
    HTML_markup = models.TextField(verbose_name='HTML разметка для интерактивного изображения',
                                   help_text='area shape="rect" coords="82,186,101,202" href="#line18" onclick="showHide("#line18");" alt="18"',
                                    blank=True, null=True)
    position = models.CharField(
        max_length=200, verbose_name='Позиция', blank=True, null=True)
    notes = models.CharField(
        max_length=600, verbose_name='Примечание', blank=True, null=True)
    marks = models.CharField(
        max_length=600, verbose_name='Маркировки', blank=True, null=True)
    guide = models.FileField(upload_to=get_image_path,
                             verbose_name='Документ pdf/excel/word')

    class Meta:
        verbose_name = u'Каталог товаров'
