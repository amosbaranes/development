from django.shortcuts import render
from .data_processing import AlgoUE
from .models import (Source, Product, YearData)


def index(request):
    title = 'UBOS Export and Import'
    sources_ = Source.objects.all()
    return render(request, 'ueconomics/index_ajax.html', {'title': title, 'sources': sources_,})
    # return render(request, 'home_djanjo.html', {})


# To update database from excel
def update_data(request):
    title = 'UBOS Export and Import'
    print('index')
    pdu = AlgoUE()
    pdu.upload_data_to_database()
    # print('data uploaded')
    products_ = Product.objects.all()
    sources_ = Source.objects.all()

    return render(request, 'ueconomics/index.html', {'title': title, 'sources': sources_,
                                                          'products': products_})


# Get data for export or import
def get_source_data(request):

    # print('-1'*100)
    # print(request.POST)
    source = request.POST.get('source')
    # print(source)
    products_ = Product.objects.all()
    print(products_)
    first_product = products_[0]
    print('-'*100)
    print(first_product)
    print('-'*100)
    source_ = Source.objects.get(type=source)
    year_data = YearData.objects.filter(source__type=source).all()
    return render(request, 'ueconomics/_index_source.html', {'source': source_, 'products': products_,
                                                             'first_product': first_product, 'year_data': year_data})

