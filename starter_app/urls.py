"""starter_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from starter_app.views import api, web

urlpatterns = [
    path('admin/', admin.site.urls),

    # web
    # path('', web.HomeView.as_view())
    # path('contacts', web.ContactsView.as_view())
    # path('contacts/<id>', web.ContactsView.as_view())

    # api
    path('api/', include([
        path('contacts.list', api.ContactsListView.as_view()),
        path('contacts.info', api.ContactsInfoView.as_view()),
        path('contacts.create', api.ContactsCreateView.as_view()),
    ]))
]
