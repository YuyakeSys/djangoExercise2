from django.shortcuts import render, redirect

from app01 import models
from app01.utils.form import NumberModelForm, NumberEditModelForm
from app01.utils.pagination import Pagination


def number_list(request):
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    page_string = page_object.html()
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,
        "page_string": page_string
    }

    return render(request, 'pretty_list.html', context)


def num_add(request):
    if request.method == 'GET':
        form = NumberModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = NumberModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/num/list/')
    return render(request, 'pretty_add.html', {'form': form})


def num_edit(req, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if req.method == 'GET':
        form = NumberEditModelForm(instance=row_object)
        return render(req, 'pretty_edit.html', {"form": form})

    form = NumberEditModelForm(data=req.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/num/list')

    return render(req, 'pretty_edit.html', {"form": form})