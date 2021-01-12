# django 默认是mysqldb,但兼容性不好，需要切换为pymysql
import pymysql

# 指定pymysql的版本
pymysql.version_info = (1,4,13,"final",0)
pymysql.install_as_MySQLdb()