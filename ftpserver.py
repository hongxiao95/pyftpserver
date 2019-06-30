#coding:utf-8

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

#实例化虚拟用户，这是FTP验证首要条件
authorizer = DummyAuthorizer()

#添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
authorizer.add_user('chongyue', '87673', 'C:\\Users\\hongx\\Documents\\TempFileShare\\', perm='elradfmw')

#添加匿名用户 只需要路径
# authorizer.add_anonymous('./')

#初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer

#添加被动端口范围
handler.passive_ports = range(2122,2123)

#监听ip 和 端口
server = FTPServer(('192.168.3.9', 10021), handler)

#开始服务
server.serve_forever()