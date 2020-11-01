 # -*- coding: utf-8 -*-

from django.db import models
import string
import datetime
from django.shortcuts import render
from django.http import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files.base import ContentFile
from django.template import RequestContext
import json
import PyPDF2
from pytils import translit
import os
from django.db.models import signals
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image

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
    


# Create your models here.
class News(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["images/",translit.slugify(filename.strip()),'.',ext])
        return path
    
    title = models.CharField(max_length = 200, verbose_name='Заголовок')
    img = models.ImageField(upload_to=get_image_path, verbose_name='Фото')
    date = models.CharField(max_length = 30, verbose_name='Дата публикации', blank = True)
    longDescription = models.TextField(verbose_name='Описание')
    shortDescription = models.CharField(max_length = 200, verbose_name='Короткое описание')
    visible = models.BooleanField(default=True, verbose_name='Показывать новость')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'Новость'
        verbose_name_plural = u'Новости'

    def __str__(self):
        return self.title

class PopularUrl(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["images/",translit.slugify(filename.strip()),'.',ext])
        return path
    
    title = models.CharField(max_length = 200, verbose_name='Заголовок')
    img = models.ImageField(upload_to=get_image_path, verbose_name='Фото')
    shortDescription = models.CharField(max_length = 400, verbose_name='Короткое описание')
    uri = models.CharField(max_length = 200, verbose_name='Ссылка на источник')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление (автозаполнение)')

    class Meta:
        verbose_name = u'Популярное'
        verbose_name_plural = u'Популярное'

    def __str__(self):
        return self.title

class Documents(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["docs/",translit.slugify(filename.strip()),'.',ext])
        return path
    
    name = models.CharField(max_length = 200, verbose_name='Название')
    data = models.FileField(upload_to=get_image_path, verbose_name='Документ pdf/excel')
    date = models.CharField(max_length = 30, verbose_name='Дата публикации', blank = True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавление (автозаполнение)')
    
    class Meta:
        verbose_name = u'Документ (Загрузки)'
        verbose_name_plural = u'Документы (Загрузки)'

    def __str__(self):
        return self.name

class SeriesEngine(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["SeriesEngine_images/",translit.slugify(filename.strip()),'.',ext])
        return path
    
    name = models.CharField(max_length = 200, verbose_name='Название')
    manufactur = models.CharField(max_length = 200, verbose_name='Завод производитель', blank=True)
    img = models.ImageField(upload_to=get_image_path, verbose_name='Фото', blank=True, null=True)
    

    class Meta:
        verbose_name = u'Серия двигателя'
        verbose_name_plural = u'Серия двигателей'

    def __str__(self):
        return self.name

class Engine(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["Engine_images/",translit.slugify(filename.strip()),'.',ext])
        return path

    def get_filePDF_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["GuidesForEngines/",translit.slugify(filename.strip()),'.',ext])
        return path
    
    seriesEngine = models.ForeignKey(SeriesEngine, on_delete=models.CASCADE, verbose_name = 'Серия двигателя', blank=True, null=True)
    name = models.CharField(max_length = 200, verbose_name='Название')
    img = models.ImageField(upload_to=get_image_path, verbose_name='Схема', blank=True, null=True)
    filePDF = models.FileField(storage=fs, upload_to=get_filePDF_path, verbose_name='Документ pdf', blank=True, null=True, default='default_pdf.pdf')
    processed = models.BooleanField(default=False, verbose_name='Без пароля и водяного знака')

    def filename(self):
        return os.path.basename(self.filePDF.name)

    class Meta:
        verbose_name = u'Название Двигателя'
        verbose_name_plural = u'Название Двигателей'

    def __str__(self):
        return self.name

@receiver(signals.post_save, sender=Engine)
def create_new_pdf_engine(sender, instance, created, **kwargs):
    if not getattr(instance, 'processed', False):
        file_url = str(media_url) + '/' + str(instance.filePDF)
        watermark_file_url = str(media_url) + '/' + 'comalfa_watermark.pdf'

        file = open(file_url, 'rb')
        # file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + instance.guide.url, 'rb')
        watermark = open(watermark_file_url, 'rb')
        # watermark = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + '/media/comalfa_watermark.pdf', 'rb')
        reader = PyPDF2.PdfFileReader(file)
        page = reader.getPage(0)
        reader2 = PyPDF2.PdfFileReader(watermark)
        waterpage = reader2.getPage(0)
        page.mergePage(waterpage)
        writer = PyPDF2.PdfFileWriter()
        writer.addPage(page)

        for pageNum in range(1, reader.getNumPages()):
            pageObj = reader.getPage(pageNum)
            pageObj.mergePage(waterpage)
            writer.addPage(pageObj)

        resultFile = open(file_url + 'watermarked.pdf', 'wb')
        # resultFile = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + instance.guide.url + 'watermarked.pdf', 'wb')
        writer.encrypt("Aa292807", use_128bit=True)
        writer.write(resultFile)
        file.close()
        watermark.close()
        resultFile.close()
        new_file_path = resultFile.name.split('/')[-1]
        instance.filePDF.name = 'GuidesForEngines/' + new_file_path
        instance.processed = True
        instance.save()

class EngineUnits(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["EngineUnits_images/",translit.slugify(filename.strip()),'.',ext])
        return path
    
    engine_name = models.ForeignKey(Engine, on_delete=models.CASCADE, verbose_name = 'Двигатель')
    name = models.CharField(max_length = 200, verbose_name='Название')
    img = models.ImageField(upload_to=get_image_path, verbose_name='Схема', blank=True)
    HTML_markup = models.TextField(verbose_name='HTML разметка для интерактивного изображения', help_text='area shape="rect" coords="82,186,101,202" href="#line18" onclick="showHide("#line18");" alt="18"', blank=True, null=True)
    sort_id = models.PositiveIntegerField(verbose_name='Порядковый номер', blank=True, null=True)
    
    class Meta:
        verbose_name = u'Деталь Двигателя'
        verbose_name_plural = u'Детали Двигателей'

    def __str__(self):
        return self.name

class Parts(models.Model):
    part_unit = models.ForeignKey(EngineUnits, on_delete=models.CASCADE, verbose_name = 'Часть детали')
    name = models.CharField(max_length = 200, verbose_name='Наименование')
    position = models.CharField(max_length = 200, verbose_name='Позиция', blank=True, null=True)
    notes = models.CharField(max_length = 600, verbose_name='Примечание', blank=True, null=True)
    quantity = models.CharField(max_length = 6, verbose_name='Кол-во на двигатель', blank=True, null=True)
    marks = models.CharField(max_length = 600, verbose_name='Маркировки', blank=True, null=True)
    
    class Meta:
        verbose_name = u'Часть детали'
        verbose_name_plural = u'Части деталей'

    def __str__(self):
        return self.name
    
class Gallery(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["Gallery_images/",translit.slugify(filename.strip()),'.',ext])
        return path

    img = models.ImageField(upload_to=get_image_path, verbose_name='Изображение')
    name = models.CharField(max_length = 200, verbose_name='Наименование')
    description = models.CharField(max_length = 200, verbose_name='Описание')

    class Meta:
        verbose_name = u'Галерея'
        verbose_name_plural = u'Галерея'

    def __str__(self):
        return self.name


class SeriesEngineGuides(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["GuidesForEngines/",translit.slugify(filename.strip()),'.',ext])

        return path

    seriesEngine = models.ForeignKey(SeriesEngine, on_delete=models.CASCADE, verbose_name = 'Серия двигателя', blank=True, null=True)
    name = models.CharField(max_length = 200, verbose_name='Название')
    guide = models.FileField(upload_to=get_image_path, verbose_name='Документ pdf/excel/word')
    processed = models.BooleanField(default=False, verbose_name='Без пароля и водяного знака')

    def save(self, *args, **kwargs):
        
        super(SeriesEngineGuides, self).save(*args, **kwargs)
    
    def filename(self):
        return os.path.basename(self.guide.name)

    class Meta:
        verbose_name = u'Руководство'
        verbose_name_plural = u'Руководства'

    def __str__(self):
        return self.name

@receiver(signals.post_save, sender=SeriesEngineGuides)
def create_customer(sender, instance, created, **kwargs):
    if not getattr(instance, 'processed', False):
        file_url = str(media_url) + '/' + str(instance.guide)
        watermark_file_url = str(media_url) + '/' + 'comalfa_watermark.pdf'

        # file = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")).replace('\\', '/') + instance.guide.url, 'rb')
        file = open(file_url, 'rb')
        # watermark = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")).replace('\\', '/') + '/media/comalfa_watermark.pdf', 'rb')
        watermark = open(watermark_file_url, 'rb')
        reader = PyPDF2.PdfFileReader(file)
        page = reader.getPage(0)
        reader2 = PyPDF2.PdfFileReader(watermark)
        waterpage = reader2.getPage(0)
        page.mergePage(waterpage)
        writer = PyPDF2.PdfFileWriter()
        writer.addPage(page)
        for pageNum in range(1, reader.getNumPages()):
            pageObj = reader.getPage(pageNum)
            pageObj.mergePage(waterpage)
            writer.addPage(pageObj)
        
        # resultFile = open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")).replace('\\', '/') + instance.guide.url + 'watermarked.pdf', 'wb')

        resultFile = open(file_url + 'watermarked.pdf', 'wb')
        writer.encrypt("Aa292807")
        writer.write(resultFile)
        file.close()
        watermark.close()
        resultFile.close()

        new_file_path = resultFile.name.split('/')[-1]
        instance.guide.name = 'GuidesForEngines/' + new_file_path
        instance.processed = True
        instance.save()

class MainGoods(models.Model):

    def get_image_path(self, filename):
        ext = filename.split('.')[-1]
        path = ''.join(["MainGoods_images/",translit.slugify(filename.strip()),'.',ext])
        return path

    GOOD_TYPES = (
        ('Подшипники', 'Подшипники'),
        ('Уплотнение клапанов', 'Уплотнение клапанов'),
        ('Компоненты впрыска', 'Компоненты впрыска'),
        ('Торцевые уплотнения', 'Торцевые уплотнения'),
        ('Прокладки', 'Прокладки'),
        ('Другое', 'Другое'),
    )
    STATUS_TYPES = (
        ('Готов', 'Готов'),
        ('В перспективе', 'В перспективе'),
        ('Удалено', 'Удалено'),
    )

    name = models.CharField(max_length = 200, verbose_name='Название', blank=True)
    mark = models.CharField(max_length = 200, verbose_name='Маркировка', blank=True)
    status = models.CharField(max_length = 200, verbose_name='Статус товара', choices=STATUS_TYPES, blank=True)
    type = models.CharField(max_length = 200, verbose_name='Тип товара', choices=GOOD_TYPES, blank=True)
    using = models.CharField(max_length = 1500, verbose_name='Применение', blank=True)
    catalogs = models.CharField(max_length = 1500, verbose_name='Каталог деталей', blank=True)
    material = models.CharField(max_length = 200, verbose_name='Материал', blank=True)
    weight = models.CharField(max_length = 200, verbose_name='Вес', blank=True)
    analog = models.CharField(max_length = 400, verbose_name='Аналоги', blank=True)
    length = models.CharField(max_length = 400, verbose_name='Размер(мм)', blank=True)
    quantity_pack = models.CharField(max_length = 200, verbose_name='Кол-во в упаковке', blank=True)
    manufactur = models.CharField(max_length = 200, verbose_name='Изготовитель', blank=True)
    package = models.CharField(max_length = 2000, verbose_name='Состав комплекта', blank=True)
    note = models.CharField(max_length = 2000, verbose_name='Примечание', blank=True)
    quantity = models.CharField(max_length = 10, verbose_name='Количество на складе', blank=True)
    price = models.CharField(max_length = 200, verbose_name='Цена без НДС', blank=True)
    discount = models.CharField(max_length = 20, verbose_name='Скидка (%)', blank=True)
    cost = models.CharField(max_length = 200, verbose_name='Цена со скидкой', blank=True)
    img = models.ImageField(upload_to=get_image_path, default='good_def_image.jpeg', verbose_name='Изображение', blank=True)

    class Meta:
        verbose_name = u'Товары'
        verbose_name_plural = u'Товары'

    def __str__(self):
        return self.name

    # def save(self):
    #     if not self.id and not self.img:
    #         return
        
    #     super(MainGoods, self).save()

    #     # image = resizeImage(self.img)
    #     image = Image.open(self.img)
    #     imageresize = image.resize((520,710), Image.ANTIALIAS)
    #     imageresize.save(self.img.path)
