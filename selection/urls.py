
from . import views
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='register'),
    path('reg_form/', views.register, name='reg_form'),
    path('login/', views.user_login, name='login'),
    path('warden_login/', views.warden_login, name='warden_login'),
    path('warden_dues/', views.warden_dues, name='warden_dues'),
    path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
    path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
    path('hostels/<slug:hostel_name>/', views.hostel_detail_view, name='hostel'),
    path('login/edit/', views.edit, name='edit'),
    path('login/select/', views.select, name='select'),
    path('logout/', views.logout_view, name='logout'),
    path('reg_form/login/edit/', views.edit, name='update'),
    path('Hostel3', views.HOSTEL3, name='hostel3'),
    path('Hostel2/', views.HOSTEL2, name='hostel2'),
    path('Hostel1/', views.HOSTEL1, name='hostel1'),
    path('hostel_list/', views.hostel_list, name='hostel_list'),
    path('submit_complaint/', views.submit_complaint, name='submit_complaint'),
    path('view_complaints/', views.view_complaints, name='view_complaints'),
    path('delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('register_complaints/', views.register_complaints, name='register_complaints'),
    path('update_complaint/<int:complaint_id>', views.update_complaint, name='update_complaint'),
    path('warden_view_complaints/', views.warden_view_complaints, name='warden_view_complaints'),
    path('warden_delete_complaint/<int:complaint_id>/', views.warden_delete_complaint, name='warden_delete_complaint'),

   

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 