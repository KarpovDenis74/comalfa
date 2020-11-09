from django.shortcuts import render
from main.models import *
from .models import *
from .forms import SearchForm

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models.functions import Lower
from django.db.models import Q


class CatalogView:

    def view_id(request, catalog_id):
        # Выбираем деталь из кататога по id
        detail = Catalog.objects.get(pk=catalog_id)
        print(detail)
        # Выбираем детали, из которых состоит рассматриваемая деталь
        details_down = MultipleParts.objects.select_related('parts').filter(
            multiple=detail).order_by('sort_id')
        # Выбираем детали, в которые входит выбранная деталь            
        details_up = MultipleParts.objects.select_related('multiple').filter(parts=detail)
        print(details_up)

        context = {}
        context['parts'] = details_down
        context['units'] = details_up
        context['curr_unit'] = detail
        context['curr_engine'] = detail.name
        return render(request, 'alfa/category_full.html', context)

    def view(request):
        context = {}
        if request.method != 'POST':
            form = SearchForm()
            context['form'] = form
            return render(request, 'alfa/search.html', context)

        form = SearchForm(request.POST)
        if form.is_valid():
            name_origin = form.cleaned_data['name']
            name_lover = name_origin.lower()
            name_upper1 = name_origin[0].upper() + name_origin[1:]
            name_upper = name_origin.upper()
            context['units'] = Catalog.objects.filter(
                Q(name__contains=name_origin) |
                Q(name__contains=name_lover) |
                Q(name__contains=name_upper1) |
                Q(name__contains=name_upper))
            context['form'] = form
        return render(request, 'alfa/search.html', context=context)

    def db_migrate_SeriesEngine(request):
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
                set_insert.append({'append': f'Объект {name}'})
                if not flag:
                    set_insert.append({'append': f'    Уже существует в базе'
                        f' объект с именем {name}'})
                else:
                    set_insert.append({'append': f'    Создан успешно'
                        f' объект с именем {name}'})
            except:
                set_insert.append({'append': f'    Ошибка при запросе'
                    f' объекта с именем {name}'})
        context = {}
        context['bd'] = 'SeriesEngine'
        context['append'] = set_insert
        return render(
                request,
                'alfa/db_migrate.html',
                context
                )


    def db_migrate_Engine(request):
        set_insert = []
        engines = Engine.objects.all()
        for engine in engines:
            name = engine.name
            scheme = engine.img
            filePDF = engine.filePDF
            processed = engine.processed
            try:
                query_get, flag = Catalog.objects.get_or_create(
                    name=name,
                    defaults={'processed': processed,
                    'scheme': scheme,
                    'filePDF': filePDF})
                set_insert.append({'append': f'Объект {name}'})
                if not flag:
                    set_insert.append({'append': '-    Уже существует'
                        f' в базе объект с именем {name}'})
                else:
                    set_insert.append({'append': '-    Создан успешно'
                        f' объект с именем {name}'})
            except:
                set_insert.append({'append': f'-    Ошибка при запросе'
                    f' объекта с именем {name}'})
            series_engine = engine.seriesEngine
            if series_engine is None:
                continue

            try:
                multiple = Catalog.objects.filter(name=series_engine.name).first()
                parts = Catalog.objects.filter(name=engine.name).first()
                quantity = int(1)
                set_insert.append({'append': f'-    Объекты найдены {multiple.name} '
                    f'и {parts.name}. Пытаемся создать связь'})
                MultipleParts.objects.create(multiple=multiple, parts=parts, quantity=quantity)
                set_insert.append({'append': f'-    Связь для объектов создана:'
                    f' {multiple.name} и {parts.name}.'})
            except:
                set_insert.append({'append': f'-    Ошибка при запросе или создании связи между объектами:'
                    f' {multiple.name} и {parts.name}.'})
        context = {}
        context['bd'] = 'Engine'
        context['append'] = set_insert
        return render(
                request,
                'alfa/db_migrate.html',
                context
                )

    def db_migrate_EngineUnits(request):
        set_insert = []
        engine_units = EngineUnits.objects.all()
        for engine_units_item in engine_units:
            name = engine_units_item.name
            scheme = engine_units_item.img
            HTML_markup = engine_units_item.HTML_markup
            try:
                set_insert.append({'append': f'Объект {name}'})
                query_get, flag = Catalog.objects.get_or_create(
                    name=name,
                    defaults={'scheme': scheme,
                        'HTML_markup': HTML_markup})
                if not flag:
                    set_insert.append({'append': f'-    Уже существует в базе'
                        f' объект с именем {name}'})
                if query_get is None:
                    set_insert.append({'append': f'-    Создан успешно'
                        f' объект с именем {name}'})
            except:
                set_insert.append({'append': f'-    Ошибка при запросе'
                    f' объекта с именем {name}'})
            engine = engine_units_item.engine_name  # Двигатель из старого каталога Engine
            catalog = Catalog.objects.filter(name=engine.name).first()     # Находим двигатель в новом каталоге Catalog по имени name
            if catalog is None:
                continue
            try:
                multiple = catalog
                parts = Catalog.objects.filter(name=engine_units_item.name).first()
                quantity = int(1)
                sort_id = engine_units_item.sort_id
                set_insert.append({'append': f'-    Объекты найдены {multiple.name} '
                    f'и {parts.name}. Пытаемся создать связь'})
                MultipleParts.objects.create(multiple=multiple,
                    parts=parts, quantity=quantity,
                    sort_id=sort_id)
                set_insert.append({'append': f'-    Связь для объектов создана:'
                    f' {multiple.name} и {parts.name}.'})
            except:
                set_insert.append({'append': f'-    Ошибка при запросе или создании связи между объектами:'
                    f' {multiple.name} и {parts.name}.'})
        context = {}
        context['bd'] = 'EngineUnits'
        context['append'] = set_insert
        return render(
                request,
                'alfa/db_migrate.html',
                context
                )


    def db_migrate_Parts(request):
        set_insert = []
        parts = Parts.objects.all()
        for parts_item in parts:
            name = parts_item.name
            position = parts_item.position
            notes = parts_item.notes
            quantity = parts_item.quantity
            marks = parts_item.marks
            try:
                set_insert.append({'append': f'Объект {name}'})
                query_get, flag = Catalog.objects.get_or_create(
                    name=name,
                    marks=marks, 
                    defaults={'position': position,
                        'notes': notes
                        })
                if not flag:
                    set_insert.append({'append': f'Уже существует в базе'
                        f' объект с именем {name}'})
                if query_get is None:
                    set_insert.append({'append': f'Создан успешно'
                        f' объект с именем {name}'})
            except:
                set_insert.append({'append': f'Ошибка при запросе'
                    f' объекта с именем {name}'})
            engine_units = parts_item.part_unit  # Часть Двигател из старого каталога EngineUnits
            catalog = Catalog.objects.filter(name=engine_units.name).first()    # Находим часть двигателя в новом каталоге Catalog по имени name
            if catalog is None:
                continue
            try:
                multiple = catalog
                parts = Catalog.objects.filter(name=name, marks=marks).first()
                set_insert.append({'append': f'-    Объекты найдены {multiple.name} '
                    f'и {parts.name}. Пытаемся создать связь'})
                MultipleParts.objects.create(multiple=multiple,
                    parts=parts, quantity=quantity)
                set_insert.append({'append': f'-    Связь для объектов создана:'
                    f' {multiple.name} и {parts.name}.'})
            except:
                set_insert.append({'append': f'-    Ошибка при запросе или создании связи между объектами:'
                    f' {multiple.name} и {parts.name}.'})
        context = {}
        context['bd'] = 'Parts'
        context['append'] = set_insert
        return render(
                request,
                'alfa/db_migrate.html',
                context
                )

    def db_migrate_SeriesEngineGuides(request):
        set_error = []
        set_insert = []
        # guides = SeriesEngineGuides.objects.all()
        # for guides_item in guides:
        #     name = guides_item.name
        #     guide = guides_item.guide
        #     processed = guides_item.processed
        #     series = guides_item.seriesEngine  # обект SeriesEngine старой базы
        #     catalog = Catalog.objects.get(name=series.name)
        #     if catalog is None:
        #         set_error.append({'error': f'Не найден объект'
        #                 f' в каталоге с именем {name}'})
        #     try:
        #         catalog.

        #         query_get, flag = Catalog.objects.get_or_create(
        #             name=name,
        #             manufactur=manufactur,
        #             defaults={'img': img})
        #         if not flag:
        #             set_error.append({'error': f'Уже существует в базе'
        #                 f' объект с именем {name}'})
        #         if query_get is None:
        #             set_insert.append({'append': f'Создан успешно'
        #                 f' объект с именем {name}'})
        #     except:
        #         set_error.append({'error': f'Ошибка при запросе'
        #             f' объекта с именем {name}'})


        # context = {}
        # context['bd'] = 'SeriesEngine'
        # context['errors'] = set_error
        # context['append'] = set_insert
        # return render(
        #         request,
        #         'alfa/db_migrate.html',
        #         context
        #         )
