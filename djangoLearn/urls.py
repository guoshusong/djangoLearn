"""djangoLearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.urls import path
from django.contrib import admin
from app01 import views


from app01 import urls

def index(request,id):
    print(request,id,type(id))


urlpatterns = [

    # 加^是为了防止 出现 aadmin这种匹配成功
    # 规定必须以admin开头
    # 加$限制以test/结尾 防止出现test/aaa
    url(r'^admin/$', admin.site.urls),
    # 自己的路由与视图函数对应的关系
    url(r'^index/', views.index),
    url(r'^login', views.login),
    url(r'^register', views.register),
    url(r'^delete_user', views.delete_user),
    url(r'^edit_user', views.edit_user),
    # 返回json
    url(r'^login_json$',views.login_json),


    # CBV
    url(r'^login', views.Login.as_view()),



    # django 2.x 3.x 变为path方法\
    # path不支持正则，但支持五种转换器和自定义转换器
    # 将第二个路由里面的内容转换为整形然后以关键字的形式传递给后面的视图函数
    path('index/<int:id>/',index),

   # url方法的第一个参数是正则表达式
    # 此情况下访问testadd会进入test 进入匹配到的第一个
    url(r'^test', views.delete_user),
    url(r'^testadd', views.edit_user),

    # 如下写法可以解决
    # 如果访问testadd django会自动重定向到testadd/
    url(r'^test/', views.delete_user),
    url(r'^testadd/', views.edit_user),

    # 无名分组
    # testadd/1314/ 会自动把 / 中间的东西作为参数，传递给后面的函数/
    url(r'^testadd/(\d+)/', views.edit_user),
    # 有名分组
    # 给正则表达式起一个别名,函数接收该值的参数变量命必须为year
    url(r'^testadd/(?P<year>\d+)/', views.edit_user),

    # 只要url前缀是app01的url，全部交给app01去处理
    include('^app01/',include(urls))



]
