from django.shortcuts import render,HttpResponse,redirect
from app01 import models


# Create your views here.



# # all
# # filter
# # get
# # first
# # last
# # values  只想拿表中的一部分属性 返回结果是列表套字典
# res = models.Department.objects.values('departmentName','departmentPwd')
# # 获取内部执行的sql语句,只能查看QuerySet对象
# print(res.query)
# # 去配置文件中配置代码,配置完成后不需要在去.query
# # values_list 返回结果是列表套元组
# # distinct 去重,去重必须是一模一样的数据
# res = models.Department.objects.values('departmentName','departmentPwd').distinct()
# # oder_by() 默认升序
# res = models.Department.objects.order_by('departmentName')
# # 降序
# res = models.Department.objects.order_by('-departmentName')
# # reverse() 反转 反转的前提是数据已经排序
# res = models.Department.objects.reverse()
# # count()
# res = models.Department.objects.count()
# # exclude() 排除在外
# res = models.Department.objects.exclude(departmentName = '')
# # exists() 是否存在
# res = models.Department.objects.filter(pk = 10).exists()
#
#
#
# # 神奇的双下划线操作
# # organizationId 大于1
# res = models.Department.objects.filter(organizationId__gt = 1)
# # 小于1
# res = models.Department.objects.filter(organizationId__lt = 1)
# # 大于等于organizationId__gte  小于等于organizationId__lte
# # id是 18 32 或者 40
# res = models.Department.objects.filter(organizationId__in = [18,32,40])
# # 18到40岁之间
# res = models.Department.objects.filter(organizationId__range=[18,40])
# # 模糊查询 名称中包含n的 默认区分大小写
# res = models.Department.objects.filter(departmentName__contains='n')
# # 忽略大小写
# res = models.Department.objects.filter(departmentName__icontains='n')
# # 以n开头
# res = models.Department.objects.filter(departmentName__startswith='n')
#
# # 如果是date类型 注册时间为1月
# res = models.Department.objects.filter(register_time__month='1')
# res = models.Department.objects.filter(register_time__year='2020')
# res = models.Department.objects.filter(register_time__year='1',)







def index(request):
    """
    :param request: request:请求所有的数据 request是一个对象
    :return:
    """
    # HttpResponse 返回字符串
    # render 返回html文件
    # redirect 重定向
    return HttpResponse("Hello")


def login(request):
    """

    :param request:
    :return:
    """


    request.path()
    request.path_info()
    # 上面两个方法只能拿到路由，没办法拿到路由后面的参数 /app

    # 下面能拿到包括参数的路由 /app?username=1
    request.get_full_path()
    request.get_full_path_info()


    # 获取请求方式 GET / POST / ... 全大写字符串
    print(request.method)
    if request.method == 'GET':
    #  获取url后面携带的参数
        request.GET.get('username')
    #   和post处理一摸一样
    elif request.method == 'POST':
        departmentName = request.POST.get('departmentName')
        departmentPwd = request.POST.get('departmentPwd')
    #     去数据库查询
    from app01 import models
    # 拿到是个列表套数据对象 [数据对象]
    # 支持索引，切片 不支持负数操作,但是不推荐用索引的方式
    # select * from user where departmentName = '' and departmentPwd = ''; filter 括号内可以携带多个关系，默认是and
    # res = models.Department.objects.filter(departmentName = departmentName)
    # department = res[0]
    department = models.Department.objects.filter(departmentName = departmentName,departmentPwd = departmentPwd).first()

    # 不推荐用get方法(若数据不存在,则方法直接报错),而filter不会
    department = models.Department.objects.get(departmentName = departmentName,departmentPwd = departmentPwd)
    print(department)
    if department == None:
        return HttpResponse('用户民不存在或密码错误')
    return HttpResponse('登录成功')

    # 查看所有的
    # 1 什么都不写
    department = models.Department.objects.filter()
    # 2 查询所有的
    department = models.Department.objects.all()
    #

def register(request):
    if request.method == 'POST':
        departmentName = request.POST.get('departmentName')
        departmentPwd = request.POST.get('departmentPwd')
        # 第一种增加方式
        res = models.Department.objects.create(departmentName = departmentName,departmentPwd = departmentPwd,organizationId = 0)
        # 第二种 利用对象的方法
        # 新建一个对象
        department = models.Department(departmentName = departmentName,departmentPwd = departmentPwd,organizationId = 0)
        # 将这一条记录所有字段都更新一遍，无论是否修改
        department.save()
        #
        print(res)


def edit_user(request):
    departmentId = request.POST.get('departmentId')
    departmentName = request.POST.get('departmentName')
    departmentPwd = request.POST.get('departmentPwd')
    # 修改数据
    # 将filter查出的对象全部更新(批量更新)
    models.Department.objects.filter(departmentId = departmentId).update(departmentName = departmentName,departmentPwd = departmentPwd)

    # 修改数据
    department = models.Department.objects.filter(departmentId = departmentId).first()
    department.departmentName = departmentName
    department.departmentPwd = departmentPwd
    department.save()
    return None


def delete_user(request):
    departmentId = request.POST.get('departmentId')
    # 批量删除
    models.Department.objects.filter(epartmentId = departmentId).delete()
    # pk会自动查到当前表的主键字段
    models.Department.objects.filter(pk = departmentId).delete()
    return None


import json
from django.http import JsonResponse
def login_json(request):
    departmentId = request.POST.get('departmentId')
    department = models.Department.objects.filter(departmentId = departmentId).first()
    department_json = {'departmentId':departmentId,'departmentName':department.departmentName,'departmentPwd':department.departmentPwd}
    # 禁止对中文进行编码
    # json_str = json.dumps(department_json,ensure_ascii=False)
    # return HttpResponse(json_str)

    # 禁止对中文进行编码
    # safe =False 允许对列表进行序列化
    return JsonResponse(department,json_dumps_params={'ensure_ascii': False},safe=False)

def uploadFile(request):
    # 获取文件
    # 文件对象
    file_obj = request.FILES.get('file')
    # 文件名字
    file_obj.name
    with open(file_obj.name,'wb') as f:
        # chunks切片
        for line in file_obj.chunks():
            f.write(line)
    return None


# CBV 视图层不用函数而是用类
from django.views import View
class Login(View):
    def get(self,request):
        pass
    def post(self,request):
        pass