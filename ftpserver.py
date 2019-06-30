#coding:utf-8

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def main():
    username = None
    passwd = None
    initport = None
    passiveport = None
    ftpdir = None
    selfip = None

    config = getConfig()
    if not config:
        handleErrorExit(config)

    try:
        username = config["username"]
        passwd = config["passwd"]
        initport = int(config["initport"])
        passiveport = int(config["passiveport"])
        ftpdir = config["ftpdir"]
        selfip = config["selfip"]

    except Exception as error:
        handleErrorExit(config)

    #实例化虚拟用户，这是FTP验证首要条件
    authorizer = DummyAuthorizer()
    #添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
    authorizer.add_user(username, passwd, ftpdir, perm='elradfmw')
    #添加匿名用户 只需要路径
    # authorizer.add_anonymous('./')

    #初始化ftp句柄
    handler = FTPHandler
    handler.authorizer = authorizer
    #添加被动端口范围
    handler.passive_ports = range(passiveport, passiveport+1)
    #监听ip 和 端口
    server = FTPServer((selfip, initport), handler)
    #开始服务
    server.serve_forever()

def getConfig():
    config = dict()
    config["username"] = ""
    config["passwd"] = ""
    config["initport"] = ""
    config["passiveport"] = ""
    config["ftpdir"] = ""
    config["selfip"] = ""

    configFile = open("./server.conf")

    line = configFile.readline()
    while line != "":
        line = line.strip()
        items = [item.strip() for item in line.split("=")]
        if items[0] in config:
            config[items[0]] = items[1]
        line = configFile.readline()
    
    if "" in config.values():
        handleErrorExit()

    return config

def handleErrorExit(msg = "No msg"):
    print("error config, exit\n Config: " + str(msg))
    exit()


if __name__ == "__main__":
    main()
