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
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


fs = FileSystemStorage(location=settings.MEDIA_ROOT)
media_url = str(settings.MEDIA_ROOT)

def resizeImage(img):
    image = Image.open(img)
    (width, height) = image.size
    if (800 / width < 800 / height):
        factor = 800 / height
    else:
        factor = 800 / width
    size = ( width / factor, height / factor)
    return image.resize(size, Image.ANTIALIAS)


class Catalog(models.Model):
    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["Alfa_catalog_images/", translit.slugify(filename.strip()), '.', ext])

    def get_guide_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["Alfa_guide_images/", translit.slugify(filename.strip()), '.', ext])

    def get_scheme_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["Alfa_scheme_images/", translit.slugify(filename.strip()), '.', ext])


    def filename(self):
        return os.path.basename(self.filePDF.name)
    
    def get_filePDF_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(
            ["Alfa_engines_guides/", translit.slugify(filename.strip()), '.', ext])
        return path

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, verbose_name='Название')
    manufactur = models.CharField(
        max_length=200, verbose_name='Завод производитель', blank=True)
    series = models.CharField(max_length=200, verbose_name='Серия')
#  SeriesEngine.img из main
    img = models.ImageField(upload_to=get_image_path,
                            verbose_name='Фото', blank=True, null=True)
# Engine.img  и из EngineUnits.img из main
    scheme = models.ImageField(upload_to=get_scheme_path,
                            verbose_name='Схема', blank=True, null=True)        
    filePDF = models.FileField(storage=fs, upload_to=get_filePDF_path,
                               verbose_name='Документ pdf', blank=True,
                               null=True, default='default_pdf.pdf')
    processed = models.BooleanField(
        default=False, verbose_name='Без пароля и водяного знака')
    HTML_markup = models.TextField(
        verbose_name='HTML разметка для интерактивного изображения',
        help_text='area shape="rect" coords="82,186,101,202" href="#line18" onclick="showHide("#line18");" alt="18"',
        blank=True, null=True)
    position = models.CharField(
        max_length=200, verbose_name='Позиция', blank=True, null=True)
    notes = models.CharField(
        max_length=600, verbose_name='Примечание', blank=True, null=True)
    marks = models.CharField(
        max_length=600, verbose_name='Маркировки', blank=True, null=True)
    guide = models.FileField(upload_to=get_guide_path,
                             verbose_name='Документ pdf/excel/word')


class MultipleParts(models.Model):
    multiple = models.ForeignKey(
        Catalog, 
        on_delete=models.CASCADE, 
        verbose_name='Состовной элемент', 
        blank=False, 
        related_name='multiple')
    parts= models.ForeignKey(
        Catalog, on_delete=models.CASCADE, verbose_name='Деталь составного элемента', blank=False, related_name='part')
    quantity = models.PositiveIntegerField(verbose_name='Количество', blank=False)
    sort_id = models.PositiveIntegerField(verbose_name='Порядковый номер', blank=True, null=True)

    def __str__(self):
        return self.count

    class Meta:       
        verbose_name = u'Составной элемент'
        verbose_name_plural = u'Составные элементы'
        unique_together = ("multiple", "parts")