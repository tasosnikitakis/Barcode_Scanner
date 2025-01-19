from django.views.generic import TemplateView
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
# from django.conf.urls.static import static
# from django.views.static import serve
# from scanner import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scanner.urls')),
    re_path(r'^(?!static/|api(?:/|$)|admin(?:/|$)).*$', TemplateView.as_view(template_name="index.html")),

]

