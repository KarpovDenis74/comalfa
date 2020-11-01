from django.shortcuts import render
from main.models import *
from .models import *

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse


class CatalogView:
    def view(request, catalog_id):
        if catalog_id is None:
            pass

    def db_migrate_Engine(request):
        set_error = []
        set_insert = []
        engines = Engine.objects.all()
        for engine in engines:
            name = engine.name
            img = engine.img
            filePDF = engine.filePDF
            processed = engine.processed
            try:
                query_get, flag = Catalog.objects.get_or_create(
                    name=name,
                    defaults={'processed': processed,
                    'img': img,
                    'filePDF': filePDF})
                if not flag:
                    set_error.append({'error': f'Уже существует в базе объект с именем {name}'})
                if query_get is None:
                    set_insert.append({'append': f'Создан успешно объект с именем {name}'})
            except:
                set_error.append({'errors': f'Ошибка при запросе объекта с именем {name}'})
        context = {}
        context['bd'] = 'Engine'
        context['errors'] = set_error
        context['append'] = set_insert
        return render(
                request,
                'alfa/db_migrate.html',
                context
                )

    def db_migrate_SeriesEngine(request):
        set_error = []
        set_insert = []
        series = SeriesEngine.objects.all()
        for series_item in series:
            name = series_item.name
            manufactur = series_item.manufactur
            img = series_item.img
            try:
                query_get, flag = Catalog.objects.get_or_create(
                    name=name,
                    manufactur=manufactur,
                    defaults={'img': img})
                if not flag:
                    set_error.append({'error': f'Уже существует в базе'
                        f' объект с именем {name}'})
                if query_get is None:
                    set_insert.append({'append': f'Создан успешно'
                        f' объект с именем {name}'})
            except:
                set_error.append({'error': f'Ошибка при запросе'
                    f' объекта с именем {name}'})
            engines = Engine.objects.filter(seriesEngine=series_item)
            if engines is None:
                continue
            for engines_item in engines:
                try:
                    multiple = Catalog.objects.filter(name=engines_item.name).first()
                    parts = Catalog.objects.filter(name=series_item.name,
                        manufactur=series_item.manufactur).first()
                    quantity = int(1)

                    set_insert.append({'append': f'Объекты найдены {multiple.name} '
                        f'и {parts.name}. Пытаемся создать связь'})
                    MultipleParts.objects.create(multiple=multiple, parts=parts, quantity=quantity)
                    set_insert.append({'append': f'Связь для объектов создана:'
                        f' {multiple.name} и {parts.name}.'})
                except:
                    set_error.append({'error': f'Ошибка при запросе или создании связи между объектами:'
                        f' {multiple.name} и {parts.name}.'})
        context = {}
        context['bd'] = 'SeriesEngine'
        context['errors'] = set_error
        context['append'] = set_insert
        return render(
                request,
                'alfa/db_migrate.html',
                context
                )