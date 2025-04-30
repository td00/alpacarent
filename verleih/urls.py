from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.startseite, name='index'),
    path('ausleihe/', views.ausleihen, name='ausleihe'),
    path('rueckgabe/', views.rueckgabe, name='rueckgabe'),
    path('user/', views.person_anlegen, name='person_anlegen'),
    path('beenden/', views.beenden, name='beenden'),
    path('beenden_force', views.beenden_force, name='beenden_force'),
    path('verfuegbar/', views.verfuegbare_assets, name='verfuegbar'),
    path('ausgegeben/', views.ausgegebene_assets, name='ausgegeben'),
    path('login/', LoginView.as_view(template_name='verleih/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('import-snipeit/', views.import_assets_view, name='import_snipeit'),
    path('meingeraet/', views.meingeraet_view, name='meingeraet'),
    path('asset-check/', views.asset_check_view, name='asset_check'),

]
