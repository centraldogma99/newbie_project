from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('<int:year>/<int:month>', views.index, name='index'),
    path('calbuilder', views.calbuilder, name='calbuilder'),
    path('listevent', views.listevent, name='listevent'),
    path('makeevent', views.makeevent, name='makeevent'),
    path('signup', views.signup, name='signup'),
    path('detailevent', views.detailevent, name='detailevent'),
    path('event/<int:pk>/', views.detailevent, name='detailevent'),
    path('event_remove', views.event_remove, name='event_remove'),
    path('event/<int:pk>/remove', views.event_remove, name='event_remove'),
    path('event_edit', views.event_edit, name='event_edit'),
    path('event/<int:pk>/edit', views.event_edit, name='event_edit'),
]
