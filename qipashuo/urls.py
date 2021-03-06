"""qipashuo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('del/<userid>/',views.del_user,name='delete_user'),
    path('del/<userid>/', views.del_user, name='delete_user'),
    # path('polls/', include('qipashuo.urls')),
    path('speakers', views.getPersonTable),
    path('ruby', views.getRuby),
    path('gf', views.grandFinal),
    path('submit_ballot_gf', views.submit_ballot_GF),
    path('users_public', views.peoplePublic),
    path('users', views.people),
    #path('', views.root_main,name='root'),
    path('', views.grandFinal),
    path('results', views.resultShow),
    path('submit_ballot_init',views.submit_ballot_init),
    path('results/speaker',views.getSpeakerRankTable),
    re_path(r'^poll/(?P<round_num>\d+)?$', views.BallotView,name='root'),
    path('submitballot', views.submit_ballot),
    path('clearall', views.clearAllUser),
]
