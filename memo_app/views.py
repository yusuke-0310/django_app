from django.shortcuts import render, redirect
from .forms import PostForm, RecordNumberForm
from .models import *
from django.core.paginator import Paginator

def index(request, now_page=1):
    if 'record_number' in request.session:
        record_number = request.session['record_number']
    else:
        record_number = 10

    record_number_form = RecordNumberForm()
    record_number_form.initial = {'record_number': str(record_number)}

    memos = Memo.objects.all().order_by('update_datetime').reverse()
    page = Paginator(memos, record_number)
    params = {
        'page': page.get_page(now_page),
        'form': PostForm(),
        'record_number_form': record_number_form,
    }
    return render(request, 'index.html', params)

def post(request):
    form = PostForm(request.POST, instance=Memo())
    if form.is_valid():
        form.save()
    else:
        print(form.errors)

    return redirect(to='/')

def set_record_number(request):
    request.session['record_number'] = request.POST['record_number']
    return redirect(to='/')