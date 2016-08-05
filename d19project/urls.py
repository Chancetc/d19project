"""d19project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from d19app import views
from django.views.static import serve

import settings

urlpatterns = [

	url(r'^$',views.home,name='home'),

    url(r'^records-stackedBar',views.records_stackedBar,name='records_stackedBar'),

    url(r'^login',views.login,name='login'),

    url(r'^signInByAction',views.signInByAction,name='signInByAction'),

    url(r'^uploadRecords',views.uploadRecords,name='uploadRecords'),

    url(r'^queryRequestForUserRecords',views.queryRequestForUserRecords,name='queryRequestForUserRecords'),

    url(r'^signInByAjaxAction',views.signInByAjaxAction,name='signInByAjaxAction'),

    url(r'^my-tags',views.my_tags,name='my_tags'),
    
    url(r'^records-by-date',views.my_dates,name='my_dates'),
    
    url(r'^queryRequetForAllRecorderTags',views.queryRequetForAllRecorderTags,name='queryRequetForAllRecorderTags'),
    
    url(r'^help',views.user_help,name='user_help'),
    
    url(r'^static/(?P<path>.*)$',serve,{ 'document_root': settings.STATIC_URL }),

    url(r'^admin/', admin.site.urls),
]
