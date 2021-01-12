from django.db import models

# Create your models here.
# 类对应的表

# 继承models.Model
# 每次修改model要执行一次
#  python manage.py makemigrations
# 将更改记录到makemigrations文件下
# python manage.py migrate
# 将操作真正的同步到数据库中
# 会自动创建表 app01_department
# 修改models.py中和数据库相关的代码，重新执行上面命令
class Department(models.Model):
    # max_length 最大长度
    # verbose_name 备注名称(所有字段都有)
    # null = True 是否为空
    # default = 设置默认值

    # 创建一个id并且是自增(当你不定义主键的时候,orm会自动帮你创建一个名为id的主键字段)
    # id int primary_key auto_increment
    departmentId = models.AutoField(primary_key=True)
    # departmentName varchar(255)
    # 必须指定max_length参数
    departmentName = models.CharField(max_length=255,verbose_name='部门名称')
    # departmentPwd varchar(255)
    departmentPwd = models.CharField(max_length=255)
    # organizationId int
    organizationId = models.IntegerField()

    # auto_now 每次操作数据的时候，该字段会自动将当前时间更新
    # auto_now_add 在创建数据的时候，自动将当前时间记录下来，一直不变
    register_time = models.DateField(auto_now=False,auto_now_add=True)
    # register_time = models.DateTimeField(auto_now=False,auto_now_add=True)


    def __str__(self):
        return '%d,%s,%s,%d' % (self.departmentId,self.departmentName,self.departmentPwd,self.organizationId)


# 外键的增删改查

class Author(models.Model):
    id = models.AutoField(primary_key =True)
    # 一对多
    author_detail = models.OneToOneField(to='Author_detail')

class Author_detail(models.Model):
    phone = models.BigIntegerField()

class Book(models.Model):
    id = models.AutoField(primary_key =True)
    title= models.CharField(max_length=255)
    Author = models.ForeignKey(to='Author')
    # 一对多
    # 外键的名称将变为 publish_对应的主键名称
    publish = models.ForeignKey(to='Publish')
    # 多对多
    authors = models.ManyToManyField(to='Author')

class Publish(models.Model):
    id = models.AutoField(primary_key =True)
    name = models.CharField(max_length=255)


def oneToMany():
    # 一对多
    # 增
    # 1.直接写实际字段 id
    models.Book.objects.create(title='123',publish_id = 1)
    # 2.虚拟字段 对象
    publish_obj = Publish.objects.filter(pk = 2).first()
    Book.objects.create(title='123',publish=publish_obj)

    # 删除
    # Publish.objects.filter(pk =1).delete() 级联删除

    # 修改
    # 1
    Book.objects.filter(pk =2).update(publish_id = 2)
    # 2
    publish_obj = Publish.objects.filter(pk=2).first()
    Book.objects.filter(pk =2).update(publish=publish_obj)

def ManyToMany():
    # 多对多
    # 操作第三张关系表
    # 虚拟表
    # 如何给书籍添加作者
    # 问题:虚拟表，没办法通过models操作
    book_obj = Book.objects.filter(pk=1).first()
    # book_obj.authors 直接到第三张表
    # 给pk为1的书籍绑定一个id为1的作者
    book_obj.authors.add(1)
    # 给pk为1的书籍绑定一个id为2,3的作者
    book_obj.authors.add(2,3)
    # 对象
    author_obj = Author.objects.filter(pk = 1).first()
    author_obj1 = Author.objects.filter(pk = 2).first()
    author_obj2 = Author.objects.filter(pk = 3).first()
    book_obj.authors.add(author_obj,author_obj1,author_obj2)


    # 删除
    book_obj.authors.remove(2)
    book_obj.authors.remove(1,3)
    book_obj.authors.remove(author_obj, author_obj1, author_obj2)

    # 修改
    # 可以传数字，也可以是对象，但必须是可迭代对象
    # 内部对应先删除再新增
    book_obj.authors.set([1,3]) # 变成book有1 3两条记录

    # 清空
    book_obj.authors.clear()


# 正反向

# 正向 看外键在谁那里 由书查作者

# 反向 由作者查书

# 多表查询

# 子查询(基于对象的跨表查询)

def select():
    # 正向
    # 1.查询书籍主键为1的出版社
    book_obj = Book.objects.filter(pk=1).first()
    book_obj.publish
    # 查询书籍为1的作者
    # 当结果可能有多个时加.all()
    book_obj.authors.all()

    # 反向
    # 查询出版社name为1出版的书
    publish = Publish.objects.filter(name = '1').first()
    # 表明小写 + _set
    res = publish.book_set.all()

    # 查询作者是jason写过的书
    author = Author.objects.filter(name = 'jason').first()

    res = author.book_set.all()

    # 结果有多个是加_set.all()
    # 查询手机号为11的作者的信息
    author_detail  = Author_detail.objects.filter(phone = '11').first()
    res = author_detail.author




    # 联表查询(基于下划线的跨表查询)
    # 查询jason的手机号 一行代码搞定
    res = Author.objects.filter(name = 'jason').values('author_detail__phone')
    # 那作者姓名是jason的作者详情
    res = Author_detail.objects.filter(author__name = 'jason').values('phone','author__id')


    # 查询书籍主键为1的出版社名称和书的名称
    res = Book.objects.filter(pk = 1).values('title','publish__name')
    res = Publish.objects.filter(book__pk = 1).values('name','book__title')

    # 查询书籍主键为1的作者id
    res = Book.objects.filter(pk = 1).values('authors__id')

    # 查询书籍主键是1的作者的手机号
    res =Book.objects.filter(pk = 1).values('authors__author_detail__phone')