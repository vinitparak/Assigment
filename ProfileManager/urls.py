from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('company_login/', views.company_login, name='company_login'),
    path('company_view/', views.company_view, name='company_view'),
    path('logout/', views.logout, name='logout'),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('manager_view/', views.manager_view, name='manager_view'),
    path('employee/<int:company_id>/<int:employee_id>', views.employee, name='employee'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#re_path(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})