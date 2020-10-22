from django.utils.deprecation import MiddlewareMixin
from .models import *

class GetReviews(MiddlewareMixin):
    def process_request(self, request):

        category_list= SeriesEngineGuides.objects.all()
        request.category_list = category_list
        print(category_list)
        return None