from django.test import TestCase

# Create your tests here.

import os


# 从manage.py文件粘贴
if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","django.settings")
    import django
    django.setup()

    # 测试代码
    # 这个from必须写在测试环境的下面
    from app01 import views



    import datetime
    ctime = datetime.datetime.now()

