from django.shortcuts import render, redirect, get_object_or_404
from django.template import Context
from django.template.loader import render_to_string
from calendar import HTMLCalendar
import calendar
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Event
from .forms import EventForm, SignupForm
import json
from datetime import date
from django.contrib.auth.decorators import login_required
import copy


def calbuilder(request):
    year = int(request.POST.get('year',None))
    month = int(request.POST.get('month',None))
    cal = HTMLCalendar(calendar.SUNDAY)
    cal = cal.formatmonth(year, month)
    cal = cal.replace('<td ', '<td class="days" width="150" height="150"')
    cal = cal.replace('border="0" cellpadding="0" cellspacing="0" class="month">','class="table">')
    events = Event.objects.filter(date__year = year, date__month = month)
    events_json = serializers.serialize('json', events)
    context = {
        'calendar':cal,
        'events':events_json
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


#첫 접속시 첫화면 출력용 뷰. 달력은 HTML 내의 AJAX가 처리한다.
def index(request, sidebarContent=None):
    #cal = HTMLCalendar(calendar.SUNDAY)
    #cal = cal.formatmonth(year, month)
    #cal = cal.replace('<td ', '<td  width="150" height="150"')
    #cal = cal.replace('border="0" cellpadding="0" cellspacing="0" class="month">','class="table">')
    if sidebarContent!=None:
        return render(request, 'cencal/index.html', {'sidebarContent':sidebarContent})
    return render(request, 'cencal/index.html')


@login_required
def makeevent(request):
    if request.method == "POST":
        print(request.POST)
        form = EventForm(request.POST)
        
        if form.is_valid():
            print("valid")
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            jsonres = JsonResponse({"res": "successful"})
            jsonres.status_code = 200
            return jsonres
        else:
            print(form.errors.as_json())
            jsonres = JsonResponse({"error": form.errors.as_json()})
            jsonres.status_code = 599
            return jsonres
    else:
        print("not post")
        form = EventForm()
        return render(request, 'cencal/eventform.html', {'form': form})

def listevent(request):
    year = int(request.POST.get('year', None))
    month = int(request.POST.get('month', None))
    day = int(request.POST.get('day', None))
    
    events = Event.objects.filter(date__exact = date(year,month,day)).order_by('start_time')
    return render(request, 'cencal/sidebar.html', {"plans":events})
    # events_json = serializers.serialize('json', events)
    # context = {
    #     'events': events_json
    # }
    # return HttpResponse(json.dumps(context), content_type = 'application/json')


def detailevent(request, pk=None):
    pk2=0
    if pk==None:
        pk2 = int(request.POST.get('pk', None))
        event = get_object_or_404(Event, pk=pk2)
    else:
        event = get_object_or_404(Event, pk=pk)
    
    return render(request, 'cencal/detailevent.html', {'event': event})

@login_required   
def event_edit(request, pk=None):
    pk2=0
    if pk==None:
        pk2 = int(request.GET.get('pk', None))
    else:
        pk2 = pk
    event = get_object_or_404(Event, pk=pk2)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            return render(request, 'cencal/index.html', {'sidebarContent':render_to_string('cencal/detailevent.html', {'event': event})})
            # return redirect('detailevent', pk=event.pk)
        else:
            # alert로 경고메시지 출력?
            return redirect('index')
    else:
        print("else")
        form = EventForm(instance=event)
        return render(request, 'cencal/eventform.html', {'form':form, 'edit':"true", 'pk':pk2})

    
@login_required
def event_remove(request, pk=None):
    pk2 = 0
    if pk==None:
        pk2 = int(request.POST.get('pk', None))
    else:
        pk2 = pk
    event = get_object_or_404(Event, pk=pk2)
    event.delete()
    return HttpResponse('')

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password')
            #user = User.objects.create_user(username=username, password=raw_password)
        return redirect("index")
    else:
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form':form})
