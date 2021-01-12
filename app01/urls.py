from django.conf.urls import url
import app01 as views


urlpatterns = [
    url(r'^login', views.login)
]
