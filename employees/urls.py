from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Employés
    path('employes/', views.employee_list, name='employee_list'),
    path('employes/ajouter/', views.employee_add, name='employee_add'),
    path('employes/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employes/<int:pk>/modifier/', views.employee_edit, name='employee_edit'),
    path('employes/<int:pk>/supprimer/', views.employee_delete, name='employee_delete'),
    path('employes/<int:pk>/data/', views.employee_data_api, name='employee_data_api'),

    # Documents
    path('employes/<int:emp_pk>/documents/ajouter/', views.document_add, name='document_add'),
    path('documents/<int:pk>/supprimer/', views.document_delete, name='document_delete'),

    # Congés
    path('conges/', views.conge_list, name='conge_list'),
    path('conges/ajouter/', views.conge_add, name='conge_add'),
    path('conges/<int:pk>/statut/<str:status>/', views.conge_update_status, name='conge_status'),

    # Paie
    path('paie/', views.paie_list, name='paie_list'),
    path('paie/ajouter/', views.paie_add, name='paie_add'),
    path('paie/<int:pk>/supprimer/', views.paie_delete, name='paie_delete'),

    # Prédictions
    path('predictions/', views.prediction_list, name='prediction_list'),
    path('predictions/ajouter/', views.prediction_add, name='prediction_add'),
    path('predictions/<int:pk>/supprimer/', views.prediction_delete, name='prediction_delete'),

    # Modèles ML
    path('modeles/', views.modele_list, name='modele_list'),
    path('modeles/ajouter/', views.modele_add, name='modele_add'),
    path('modeles/<int:pk>/supprimer/', views.modele_delete, name='modele_delete'),

    # Admin RH
    path('admin-rh/', views.admin_rh_list, name='admin_rh_list'),
    path('admin-rh/ajouter/', views.admin_rh_add, name='admin_rh_add'),
    path('admin-rh/<int:pk>/supprimer/', views.admin_rh_delete, name='admin_rh_delete'),

    # Espace Employé
    path('mon-espace/', views.espace_employe, name='espace_employe'),

    # Page RH  ✅ (ajouté)
    path('page-rh/', views.page_rh, name='page_rh'),
   
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Documents & Notifications
    path('document/delete/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('notifications/', views.notifications_api, name='notifications_api'),
    path('notifications/lu/', views.notifications_mark_read, name='notifications_mark_read'),
]
