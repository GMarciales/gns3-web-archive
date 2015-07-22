"""gns3_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
import settings
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.home', name="index"),
    url(r'^server/version/?$', 'main.views.get_server_version', name="server_version"),
    url(r'^project/create', 'main.views.create_project',name="create_project"),
    url(r'^settings/?$', 'main.views.settings', name="settings"),
    url(r'^vcps/create/?$', 'main.views.create_vcps', name='create_vcps'),
    url(r'^vcps/link/?$','main.views.link_nodes', name='link_nodes'),
    url(r'^vcps/start/?$','main.views.start_vm', name='start_vm')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
