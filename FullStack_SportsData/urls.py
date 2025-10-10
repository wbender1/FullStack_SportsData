"""
URL configuration for FullStack_SportsData project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from sportsdataapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('competitions/', views.competitions_view, name='competitions'),
    path('countries/', views.countries_view, name='countries'),
    path('fixtures/', views.fixtures_view, name='fixtures'),
    path('fixturestats/', views.fixture_stats_view, name='fixturestats'),
    path('seasons/', views.seasons_view, name='seasons'),
    path('standings/', views.standings_view, name='standings'),
    path('teams/', views.teams_view, name='teams'),
    path('venues/', views.venues_view, name='venues'),
]
