from django.shortcuts import render
from .models import Shopdata
from io import TextIOWrapper, StringIO
import csv
from datetime import datetime
from django.views import generic

class Datalist(generic.ListView):
    model = Shopdata
    template_name = 'data/data_list.html'

# class Monthlist(generic.TemplateView):
#     model = Shopdata
#     template_name = month_list
#     data_field =days

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        

def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file)
        csv_file = csv.reader(form_data)
        for line in csv_file:
            day=datetime.strptime(line[0], '%Y/%m/%d')
            
            shopdata, created = Shopdata.objects.get_or_create(days=day,shop=line[1])
            shopdata.days = day
            shopdata.shop=line[1]
            shopdata.sales = line[2]
            shopdata.gest = line[3]
            shopdata.gloup = line[4]
            shopdata.one = line[5]
            shopdata.maketime = line[7]
            shopdata.labor = line[8]
            shopdata.save()

        return render(request, 'register/top.html')

    else:
        return render(request, 'data/upload.html')