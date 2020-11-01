from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('catalog/<int:catalog_id>',
        views.CatalogView.view,
        name='catalog'),
    path('db_migrate_Engine/',
        views.CatalogView.db_migrate_Engine,
        name='db_migrate_Engine'),
    path('db_migrate_SeriesEngine/',
        views.CatalogView.db_migrate_SeriesEngine,
        name='db_migrate_SeriesEngine'),   

]
