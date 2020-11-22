from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('<int:year>/<int:month>', views.index, name='index'),
    path('calbuilder', views.calbuilder, name='calbuilder'),
    path('listevent', views.listevent, name='listevent'),
    path('makeevent', views.makeevent, name='makeevent'),
    path('detailevent', views.detailevent, name='detailevent'),
    path('signup', views.signup, name='signup')
]
