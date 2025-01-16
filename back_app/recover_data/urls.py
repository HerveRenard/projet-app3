from django.urls import path
from recover_data import views
from .views import RecevoirDonneesAPIView,DernieresDonneesAPIView
urlpatterns = [
    path('api/recevoir_donnees/', RecevoirDonneesAPIView.as_view(), name='recevoir_donnees'),
    path('api/dernieres_donnees/', DernieresDonneesAPIView.as_view(), name='dernieres_donnees'),
    path('api/connexion_eleveur/', views.connexion_api, name='connexion_eleveur'),
    path('api/inscription_eleveur/', views.inscription, name='inscription_eleveur'),
    path('api/deconnexion_eleveur/', views.deconnexion_eleveur, name='deconnexion_eleveur'),
    path('api/connexion_admin/', views.connexion_admin, name='connexion_admin'),
    path('api/codeConnexionAdmin', views.connexion_admin_code, name="codeConnexionAdmin"),
    path('api/deconnexionAdmin', views.admin_deconnexion, name="deconnexionAdmin"),
    path('api/list_eleveur', views.list_eleveur, name="list_eleveur"),
    path('api/list_boeuf', views.list_boeuf, name="list_boeuf"),
    path('api/list_donnees_boeuf', views.list_donnees_boeuf, name="list_donnees_boeuf"),
    path('api/creer_boeuf', views.creer_boeuf, name="creer_boeuf"),
    path('api/detail_eleveur', views.detail_eleveur, name="detail_eleveur"),
    path('api/detail_boeuf', views.detail_eleveur, name="detail_boeuf"),
    path('api/detail_admin', views.detail_admin, name="detail_admin"),

]