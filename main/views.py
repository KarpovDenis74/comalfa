 # -*- coding: utf-8 -*-

import string
import os
from django.conf import settings
import datetime
from django.shortcuts import render, render_to_response, redirect
from django.http import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
import base64
from django.core.files.base import ContentFile
from django.template import RequestContext
from .forms import ImageUploadForm
from .forms import UploadFileForm
from .forms import Docs_Form
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.mdb_upload import UploadMDB
from utils.excel_parse import RefreshDiscountGoods
from django.core.mail import EmailMessage
from django.template import Context

import json

from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from PIL import Image as PIL_Image  
from django.views.generic import View
from django.http import JsonResponse
from django.template import RequestContext

from pytils import translit
import ast


MAIN_EMAIL = []
MAIN_EMAIL.append('comAlfa@yandex.ru')
# MAIN_EMAIL.append('dimankaboski@mail.ru')

# Create your views here.

# HTTP Error 500
def server_error(request, *args, **argv):
    response = render_to_response('500.html')
    response.status_code = 500
    return response
    
# HTTP Error 404
def page_not_found(request, *args, **argv):
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def index(request):
    news = News.objects.filter(visible=True).order_by('-created_at')[:2]
    files = Documents.objects.filter().order_by('-created_at')[:2]
    popular = PopularUrl.objects.filter().order_by('-created_at')[:3]
    context = {}
    context['docs'] = files
    context['news'] = news
    context['popular'] = popular
    return render(request, 'index.html', context)

def news(request):
    context = {}
    news = News.objects.filter(visible=True).order_by('-created_at')
    paginator = Paginator(news, 8) # Show 25 contacts per page
    num_pages = [x for x in range(1, paginator.num_pages + 1)] 
    page = request.GET.get('page')
    try:
        context['news'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context['news'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last p
        context['news'] = paginator.page(paginator.num_pages)
    context['num_pages'] = num_pages
    return render(request, 'news.html', context)


def category(request):
    context = {}
    context['categorys'] = SeriesEngine.objects.all()
    return render(request, 'category.html', context)

def bearing(request):
    
    return render(request, 'bearing.html')

def seals(request):
    
    return render(request, 'seals.html')

def fuel(request):
    
    return render(request, 'fuel.html')

def order(request):

    return render(request, 'order.html')

def sealspump(request):
    
    return render(request, 'sealspump.html')

def gasket(request):
    
    return render(request, 'gasket.html')

def manufacturing(request):
    
    return render(request, 'manufacturing.html')

def development(request):
    
    return render(request, 'development.html')

def turning(request):
    
    return render(request, 'turning.html')

def thanks(request):
    
    return render(request, 'thanks.html')

def trade(request):
    
    return render(request, 'trade.html')

def product(request):
    
    return render(request, 'product.html')

def tender(request):

    return render(request, 'tender.html')

def pdfviewer(request, uri_pdf):
    context = {}
    try:
        context['enginePDF'] = SeriesEngineGuides.objects.get(guide__contains=uri_pdf)
    except:
        context['enginePDF'] = Engine.objects.get(filePDF__contains=uri_pdf)
 
    context['url'] = uri_pdf
    return render(request, 'pdfviewer.html', context)

def services(request):
    
    return render(request, 'services.html')

def about(request):
    
    return render(request, 'about.html')

def componentcat(request):
    
    return render(request, 'componentcat.html')

def gallery(request):
    context = {}
    imgt = Gallery.objects.all()
    paginator = Paginator(imgt, 16) # Show 25 contacts per page
    num_pages = [x for x in range(1, paginator.num_pages + 1)] 
    page = request.GET.get('page')
    try:
        context['imgs'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context['imgs'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last p
        context['imgs'] = paginator.page(paginator.num_pages)
    context['num_pages'] = num_pages
    return render(request, 'gallery.html', context)


def contact(request):
    
    return render(request, 'contact.html')

def sales(request):
    context = {}
    context['discount'] = MainGoods.objects.filter(status='Готов').exclude(cost__exact='')
    for item_use in context['discount']:
        usingWithUrl = []
        for item in item_use.using.split(','):
            nameAndUrl = item.split(":")
            if(len(nameAndUrl) > 1):
                usingWithUrl.append({nameAndUrl[0]:nameAndUrl[1]})
            else:
                usingWithUrl.append({nameAndUrl[0]:''})
        item_use.usingUrl = usingWithUrl
    return render(request, 'sales.html', context)

def perspective(request):
    context = {}
    context['perspective'] = MainGoods.objects.filter(status='В перспективе')
    for item_use in context['perspective']:
        usingWithUrl = []
        for item in item_use.using.split(','):
            nameAndUrl = item.split(":")
            if(len(nameAndUrl) > 1):
                usingWithUrl.append({nameAndUrl[0]:nameAndUrl[1]})
            else:
                usingWithUrl.append({nameAndUrl[0]:''})
        item_use.usingUrl = usingWithUrl
    return render(request, 'perspective.html', context)

def productslast(request):
    context = {}
    context['perspective'] = MainGoods.objects.filter().exclude(status='Удалено').exclude(quantity__exact='0').exclude(quantity__exact='')
    for item_use in context['perspective']:
        usingWithUrl = []
        for item in item_use.using.split(','):
            nameAndUrl = item.split(":")
            if(len(nameAndUrl) > 1):
                usingWithUrl.append({nameAndUrl[0]:nameAndUrl[1]})
            else:
                usingWithUrl.append({nameAndUrl[0]:''})
        item_use.usingUrl = usingWithUrl
    return render(request, 'productslast.html', context)
    
def productsprice(request):
    context = {}
    context['perspective'] = MainGoods.objects.exclude(status='В перспективе').exclude(status='Удалено').exclude(price__exact='')
    for item_use in context['perspective']:
        usingWithUrl = []
        for item in item_use.using.split(','):
            nameAndUrl = item.split(":")
            if(len(nameAndUrl) > 1):
                usingWithUrl.append({nameAndUrl[0]:nameAndUrl[1]})
            else:
                usingWithUrl.append({nameAndUrl[0]:''})
        item_use.usingUrl = usingWithUrl
    return render(request, 'productsprice.html', context)

def geo(request):
    return render(request, 'geo.html')

def bearingcat(request):
    return render(request, 'bearingcat.html')

def fuelcat(request):
    return render(request, 'fuelcat.html')

def sealscat(request):
    return render(request, 'sealscat.html')

def sert(request):
    return render(request, 'sert.html')

def sealspumpcat(request):
    return render(request, 'sealspumpcat.html')

def goodscatall(request):
    context = {}
    items = MainGoods.objects.filter(status='Готов')
    paginator = Paginator(items, 15) # Show 25 contacts per page
    num_pages = [x for x in range(1, paginator.num_pages + 1)] 
    page = request.GET.get('page')
    try:
        context['goods'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context['goods'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last p
        context['goods'] = paginator.page(paginator.num_pages)
    context['num_pages'] = num_pages
    return render(request, 'goodscat.html', context)

def goodscat_card(request, good_id):
    context = {}
    context['ordergoods'] = MainGoods.objects.filter().values('name', 'mark', 'id')
    context['good'] = MainGoods.objects.get(id=good_id)
    usingWithUrl = []
    catalogsWithUrl = []
    for item in context['good'].using.split(','):
        nameAndUrl = item.split(":")
        if(len(nameAndUrl) > 1):
            usingWithUrl.append({nameAndUrl[0]:nameAndUrl[1]})
        else:
            usingWithUrl.append({nameAndUrl[0]:''})
    context['using'] = usingWithUrl
    for item in context['good'].catalogs.split(','):
        nameAndUrl = item.split(":")
        if(len(nameAndUrl) > 1):
            catalogsWithUrl.append({nameAndUrl[0]:nameAndUrl[1]})
        else:
            catalogsWithUrl.append({nameAndUrl[0]:''})
    context['catalogs'] = catalogsWithUrl
    return render(request, 'goodscat_card.html', context)

def goodscat(request, good_type):
    filters_list = good_type.split('+')
    context = {}

    items = MainGoods.objects.filter(status='Готов').filter(type__in=filters_list)
    paginator = Paginator(items, 15) # Show 25 contacts per page
    num_pages = [x for x in range(1, paginator.num_pages + 1)] 
    page = request.GET.get('page')
    try:
        context['goods'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        context['goods'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last p
        context['goods'] = paginator.page(paginator.num_pages)
    context['num_pages'] = num_pages
    return render(request, 'goodscat.html', context)


class UploadImage(View):

    http_method_names = ['post']
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super(UploadImage, self).dispatch(request, *args, **kwargs)

    def get_upload_path(self, upload):
        upload_path = 'images'
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, upload_path)):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, upload_path))

        upload_filename = os.path.join(upload_path, upload.name)
        return (upload.name, os.path.join(settings.MEDIA_ROOT, upload_filename), settings.MEDIA_URL + upload_filename)

    def post(self, request, *args, **kwargs):
        if request.FILES:
            upload = request.FILES['file']
            filename, filename_root, filename_url = self.get_upload_path(upload)
            with open(filename_root, 'wb+') as out:
                for chunk in upload.chunks():
                    out.write(chunk)
            out.close()
            img = PIL_Image.open(filename_root)
            width, height = img.size
            return JsonResponse({
                'image': filename_url,
                'width': str(width),
                'height': str(height)
            })
        return HttpResponse(status=400)


class UpdateImgUnits(View):
    http_method_names = ['post']
    unit = None
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def _get_unit(self, unit_id):
        try:
            self.unit = EngineUnits.objects.get(id = unit_id)
        except:
            return None
        return self.unit

    def post(self, request, *args, **kwargs):        
        data = json.loads(str(request.body.decode('UTF-8')))
        if data["id"]:
            self._get_unit(data["id"])
            if self.unit:
                if data["img"]:
                    self.unit.img = data["img"].replace('media/','')
                if data["map"]:
                    self.unit.HTML_markup = data["map"]
                self.unit.save()
                return HttpResponse(status=200)
            return HttpResponse(status=400)
        return HttpResponse(status=400)

@csrf_exempt
def update_parts_info(request):
    if request.method == 'POST':
        response = {}
        json_string = json.loads(request.POST['json'])

        if(json_string['sort']):
            for item_sort in json_string['sort']:
                unit = EngineUnits.objects.get(id=item_sort['unit_id'])
                unit.sort_id = item_sort['sort_id']
                unit.save()
        if(json_string['parts']):
            for part in json_string['parts']:
                part_obj = Parts.objects.get(id=part['part_id'])
                part_obj.name = part['name']
                part_obj.notes = part['notes']
                part_obj.quantity = part['quantity']
                full_string_mark = ''
                # list_mark = ast.literal_eval(part['mark'])
                # list_quantity = ast.literal_eval(part['quantity_unit'])
                # list_unit = ast.literal_eval(part['unit'])
                list_mark = part['mark']
                list_quantity = part['quantity_unit']
                list_unit = part['unit']
                for i in range(0, len(list_mark)):
                    full_string_mark += list_mark[i] + ','
                    full_string_mark += list_unit[i] + ','
                    full_string_mark += list_quantity[i] + ';'
                part_obj.marks = full_string_mark
                part_obj.save()

        return JsonResponse(response, safe=False)
    else:
        return JsonResponse('false', safe=False)


def engine_units(request, category_id):
    context = {}
    engine = Engine.objects.get(id = category_id)
    context['curr_engine'] = engine
    context['units'] = EngineUnits.objects.filter(engine_name=engine).order_by('sort_id')
    return render(request, 'category_full.html', context)

def get_mark(str):
    return str.split(';')[0]

def engine_units_parts(request, category_id, unit_id):
    context = {}
    engine = Engine.objects.get(id = category_id)
    unit = EngineUnits.objects.get(engine_name=engine, id = unit_id)
    part = list(Parts.objects.filter(part_unit = unit))
    count = 0
    for pp in part:
        mark = []
        unit_m = []
        quantity_unit = []
        full_mark = part[count].marks.split(';')
        for t in full_mark:
            if t == "": continue
            mark.append(t.split(',')[0])
            unit_m.append(t.split(',')[1])
            quantity_unit.append(t.split(',')[2])
        part[count].mark = mark
        part[count].unit = unit_m
        part[count].quantity_unit = quantity_unit
        part[count].length_mark = range(1, len(mark))
        count += 1
    context['parts'] = part
    context['units'] = EngineUnits.objects.filter(engine_name=engine).order_by('sort_id')
    context['curr_unit'] = unit
    context['curr_engine'] = engine
    return render(request, 'category_full.html', context)

def engine_units_part(request, category_id, part_id, unit_id):
    context = {}
    engine = Engine.objects.get(id = category_id)
    unit = EngineUnits.objects.get(engine_name=engine, id = unit_id)
    part = Parts.objects.get(part_unit = unit, id = part_id)
    context['part'] = part
    context['curr_unit'] = unit
    context['curr_engine'] = engine
    return render(request, 'part_full.html', context)


@csrf_exempt
def get_unit_parts(request):
    if request.method == 'POST':
        response = {}
        json_string = json.loads(request.POST['json'])
        engine_unit = EngineUnits.objects.get(id=json_string['unit_id'])
        parts = list(Parts.objects.filter(part_unit=engine_unit).values('name', 'position', 'notes', 'quantity', 'marks', 'id'))
        response['parts'] = parts
        if(engine_unit.img):
            response['image'] = engine_unit.img.url

        return JsonResponse(response, safe=False)
    else:
        return JsonResponse('error', safe=False)

def news_full(request, news_id):
    context = {}
    context['news'] = News.objects.get(id = news_id)
    return render(request, 'news_full.html', context)


def download_docs(request):
    docs = Documents.objects.order_by('-created_at')
    context = {'docs':docs}
    return render(request, 'downloads.html', context)

@csrf_exempt
def fast_search(request):
    if request.method == 'POST':
        response = {}
        json_string = json.loads(request.POST['json'])
        q = json_string['query'].capitalize()
        goods = list(MainGoods.objects.filter(Q(name__icontains=q) | Q(name__icontains=json_string['query']) | Q(mark__icontains=json_string['query'].upper())).values('name', 'mark', 'id'))[:4]
        response['goods'] = goods
        return JsonResponse(response, safe=False)
    else:
        return JsonResponse('false', safe=False)



def moder_add_cat(request):

    return render(request, 'moder_add_cat.html')

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file.name = translit.slugify(file.name)
            engine_name = request.POST['engine_name']
            engine = Engine.objects.create()
            engine.name = engine_name
            engine.save()
            model_file = FileSystemStorage()
            mdb = model_file.save(file.name, file)
        except:
            return JsonResponse('file_error', safe=False)
        try:
            uploaded_file_url = model_file.url(mdb)
            upload = UploadMDB({'file': file.name, 'engine':engine})
            return JsonResponse('success', safe=False)
        except:
            return JsonResponse('parsing_error', safe=False)
        
    else:
        return JsonResponse('false', safe=False)

@csrf_exempt
def refresh_discount_goods(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file.name = translit.slugify(file.name)
            model_file = FileSystemStorage()
            excel_file = model_file.save(file.name, file)
        except:
            return JsonResponse('file_error', safe=False)
        # try:
        uploaded_file_url = model_file.url(excel_file)
        upload = RefreshDiscountGoods({'file': excel_file})
        return JsonResponse('success', safe=False)
        # except:
        #     return JsonResponse('parsing_error', safe=False)          
    else:
        return JsonResponse('false', safe=False)


@csrf_exempt
def new_order_request(request):
    if request.method == 'POST':
        cart_items = ''
        if 'cart' not in request.session:
            request.session['cart'] = {}
        goods = list(MainGoods.objects.filter(id__in=request.session['cart'].keys()).values('id', 'name', 'mark'))
        for g in goods:
            g['count'] = request.session['cart'][str(g['id'])]
            cart_items += '- {} {}, в кол-ве: {} шт. <br>'.format(g['name'], g['mark'], g['count'])
        text = 'Новый заказ от {}, эл. почта: {}<br>Текст сообщения: {}<br>{}'.format(request.POST['name'], request.POST['email'],request.POST['message'], cart_items)
        msg = EmailMessage('Новый заказ! com-alfa.ru', text, to=MAIN_EMAIL, from_email='infocomalfa@yandex.ru')
        msg.content_subtype = 'html'
        msg.send()
        BUYERS_EMAIL = []
        BUYERS_EMAIL.append(request.POST['email'])
        buyersText = 'Ваш заказ на сайте com-alfa.ru был создан. Спасибо! С вами свяжутся в ближайшее время!<br>{}'.format(cart_items)
        msg = EmailMessage('Заказ на сайте com-alfa.ru', buyersText, to=BUYERS_EMAIL, from_email='infocomalfa@yandex.ru')
        msg.content_subtype = 'html'
        msg.send()
        request.session['cart'] = {}
        # try:

        # except:

        return redirect('/thanks')
    else:
        return JsonResponse('false', safe=False)

@csrf_exempt
def new_tender_request(request):
    if request.method == 'POST':

        text = 'Заявка на участие в тендере от {}, эл. почта: {}<br>Текст сообщения: {}'.format(request.POST['name'], request.POST['email'],request.POST['message'])
        msg = EmailMessage('Тендер - заявка на участие! com-alfa.ru', text, to=MAIN_EMAIL, from_email='infocomalfa@yandex.ru')
        msg.content_subtype = 'html'
        msg.send()
        # try:

        # except:

        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('false', safe=False)

@csrf_exempt
def refresh_perspective_goods(request):
    if request.method == 'POST':
        file = request.FILES['file']
        model_file = FileSystemStorage()
        excel_file = model_file.save(file.name, file)
        uploaded_file_url = model_file.url(excel_file)
        upload = RefreshPerspective({'file': uploaded_file_url})

        if(upload.status == '404'):
            return JsonResponse('false', safe=False)
        else:
            return JsonResponse('success', safe=False)
        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('false', safe=False)

@csrf_exempt
def refresh_product_price(request):
    if request.method == 'POST':
        file = request.FILES['file']
        model_file = FileSystemStorage()
        excel_file = model_file.save(file.name, file)
        uploaded_file_url = model_file.url(excel_file)
        upload = RefreshProductPrice({'file': uploaded_file_url})

        if(upload.status == '404'):
            return JsonResponse('false', safe=False)
        else:
            return JsonResponse('success', safe=False)
        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('false', safe=False)

@csrf_exempt
def refresh_product_last(request):
    if request.method == 'POST':
        file = request.FILES['file']
        model_file = FileSystemStorage()
        excel_file = model_file.save(file.name, file)
        uploaded_file_url = model_file.url(excel_file)
        upload = RefreshProductLast({'file': uploaded_file_url})

        if(upload.status == '404'):
            return JsonResponse('false', safe=False)
        else:
            return JsonResponse('success', safe=False)
        return JsonResponse('success', safe=False)
    else:
        return JsonResponse('false', safe=False)

def cart(request):
    request.session.modified = True
    context = {}
    if 'cart' not in request.session:
        request.session['cart'] = {}
    goods = list(MainGoods.objects.filter(id__in=request.session['cart'].keys()).values('id', 'name', 'mark', 'price', 'quantity'))
    for g in goods:
        g['count'] = request.session['cart'][str(g['id'])]
    context['cart_g'] = goods
    return render(request, 'cart.html', context)

@csrf_exempt
def addtocart(request, good_id):
    count = 1
    request.session.modified = True
    if 'cart' not in request.session:
        request.session['cart'] = {}
    if int(good_id) not in request.session['cart']:
        request.session['cart'][str(good_id)] = count
    else:
        request.session['cart'] = {}
    return JsonResponse(request.session['cart'], safe=False)

@csrf_exempt
def gooddelete(request, good_id):
    request.session.modified = True
    request.session['cart'].pop(str(good_id), None)
    return JsonResponse(request.session['cart'], safe=False)

@csrf_exempt
def changecount(request, good_id, good_count):
    request.session.modified = True
    request.session['cart'][str(good_id)] = good_count
    return JsonResponse(request.session['cart'], safe=False)

@csrf_exempt
def getcart(request):
    request.session.modified = True
    if 'cart' not in request.session:
        request.session['cart'] = {}
    goods = list(MainGoods.objects.filter(id__in=request.session['cart'].keys()).values('id', 'name', 'mark'))
    for g in goods:
        g['count'] = request.session['cart'][str(g['id'])]
    return JsonResponse(goods, safe=False)

@csrf_exempt
def getCartCount(request):
    count = len(request.session['cart'].keys())
    return JsonResponse(count, safe=False) 