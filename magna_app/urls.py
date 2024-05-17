
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "magna_app"
urlpatterns = [
    # path('', TemplateView.as_view(template_name='index.html')),
    path('entrada', TemplateView.as_view(template_name='index.html')),
    
    # path('get_users/', views.get_users),

    # API rest
    path('usuario/<int:dni>', views.Usuario, name="usuario"),
    path('admin_usuario/<int:dni>', views.admin_usuario, name="admin_usuario"),
    path('upload_excel/', views.upload_excel, name="upload_excel"),
    
]