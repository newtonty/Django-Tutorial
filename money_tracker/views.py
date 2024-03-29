from django.shortcuts import render
from money_tracker.models import TransactionRecord
from django.http import HttpResponseRedirect
from money_tracker.forms import TransactionRecordForm
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@login_required(login_url='/money_tracker/login/')
def show_tracker(request):
    transaction_data = TransactionRecord.objects.all()
    context = {
        'list_of_transactions': transaction_data,
        'name': request.user.username,
        'last_login': request.COOKIES['last_login'],

    }
    return render(request, "tracker.html", context)

def create_transaction(request):
    form = TransactionRecordForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('money_tracker:show_tracker'))

    context = {'form': form}
    return render(request, "create_transaction.html", context)

def show_xml(request):
    data = TransactionRecord.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = TransactionRecord.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request):
    data = TransactionRecord.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request):
    data = TransactionRecord.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('money_tracker:login')

    context = {'form':form}
    return render(request, 'register.html', context)

def modify_transaction(request, id):
    # Get data berdasarkan ID
    transaction = TransactionRecord.objects.get(pk = id)

    # Set instance pada form dengan data dari transaction
    form = TransactionRecordForm(request.POST or None, instance=transaction)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('money_tracker:show_tracker'))

    context = {'form': form}
    return render(request, "modify_transaction.html", context)

def delete_transaction(request, id):
    # Get data berdasarkan ID
    transaction = TransactionRecord.objects.get(pk = id)
    # Hapus data
    transaction.delete()
    # Kembali ke halaman awal
    return HttpResponseRedirect(reverse('money_tracker:show_tracker'))

@csrf_exempt
def create_transaction_ajax(request):  
# create object of form
    form = TransactionRecordForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        data = TransactionRecord.objects.last()

        # parsing the form data into json
        result = {
            'id':data.id,
            'name':data.name,
            'type':data.type,
            'amount':data.amount,
            'date':data.date,
            'description':data.description,
        }
        return JsonResponse(result)

    context = {'form': form}
    return render(request, "create_transaction.html", context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("money_tracker:show_tracker")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('money_tracker:login'))
    response.delete_cookie('last_login')
    return response