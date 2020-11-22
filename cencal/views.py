from django.shortcuts import render, redirect
from django.template import Context
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


def calbuilder(request):
    year = int(request.POST.get('year',None))
    month = int(request.POST.get('month',None))
    cal = HTMLCalendar(calendar.SUNDAY)
    cal = cal.formatmonth(year, month)
    cal = cal.replace('<td ', '<td  width="150" height="150"')
    cal = cal.replace('border="0" cellpadding="0" cellspacing="0" class="month">','class="table">')
    events = Event.objects.filter(date__year = year, date__month = month)
    events_json = serializers.serialize('json', events)
    context = {
        'calendar':cal,
        'events':events_json
    }
    return HttpResponse(json.dumps(context), content_type="application/json")


#첫 접속시 첫화면 출력용 뷰. 달력은 HTML 내의 AJAX가 처리한다.
def index(request):
    #cal = HTMLCalendar(calendar.SUNDAY)
    #cal = cal.formatmonth(year, month)
    #cal = cal.replace('<td ', '<td  width="150" height="150"')
    #cal = cal.replace('border="0" cellpadding="0" cellspacing="0" class="month">','class="table">')
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


def detailevent(request):
    idx = int(request.POST.get('idx', None))
    date = int(request.POST.get('date', None))
    events = Event.objects.filter(date__exact = date).order_by('start_time')
    form = EventForm(request.POST, instance = events[idx])
    return render(request, 'cencal/eventform.html', {'form': form})

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
