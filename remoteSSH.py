from paramiko import SSHClient,AutoAddPolicy,ssh_exception,Transport,SFTPClient
from settings import Settings
import csv
from json import dump
from threading import Thread
from os import remove,getcwd

class RemoteSSH():
    def __init__(self):
        self.set = Settings()
        self.workPath = getcwd() + "/"
        self.servers_config_path = self.workPath+"servers.csv"


    def deploy(self):
        self.servers = self.readConfig()
        if isinstance(self.servers,list):
            print("在配置文件中找到",len(self.servers)-1,"个节点...")
            for server in self.servers[1:]:
                server = tuple(server[1:])
                Thread(target=self.execute,args=server).start()
        else:
            print("ERROR 未在当前目录下找到配置文件","servers.csv","请手动输入配置信息...")
            host = input("节点地址:")
            port = int(input("节点ssh端口:"))
            password = input("节点root密码:")
            dbHost = input("数据库地址:")
            dbPassword = input("数据库密码:")
            dbName = input("数据库名:")
            nodeID = int(input("节点node_id:"))
            remark = "默认节点"

            self.execute(remark,host,port,password,dbHost,dbPassword,dbName,nodeID)

    def readConfig(self):
        try:
            with open(self.servers_config_path) as f:
                servers = list(csv.reader(f))
                return servers
        except FileNotFoundError:
            return "No file"


    def checkConfig(self,*args):
        for arg in args[1:]:
            if arg == "":
                return False
        return True


    def execute(self,remark,host,port,password,dbHost,dbPassword,dbName,nodeID):
        if not self.checkConfig(remark,host,port,password,dbHost,dbPassword,dbName,nodeID):
            print(remark,"ERROR 节点信息不全!")
            input(self.set.tip)
            return

        print(remark,"start 开始部署...")
        try:
            int(port),int(nodeID)
        except ValueError:
            print(remark,"ERROR ssh端口或node_id只能是数字!")
            input(self.set.tip)
            return
        mysql_config_path = self.workPath+host+"_user_mysql.json"
        with open(mysql_config_path,"w",encoding="utf-8") as configFile:
            dump(self.set.generateUserMysqlFile(dbHost,dbPassword,dbName,nodeID),configFile)
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            print(remark,"waiting 正在连接节点...")
            ssh.connect(host,int(port),self.set.username,password)
        except ssh_exception.NoValidConnectionsError:
            print(remark,"ERROR 错误的端口!")
            remove(mysql_config_path)
            input(self.set.tip)
            return
        except ssh_exception.AuthenticationException:
            print(remark,"ERROR 身份认证失败!")
            remove(mysql_config_path)
            input(self.set.tip)
            return
        except TimeoutError:
            print(remark,"ERROR 节点连接超时!")
            remove(mysql_config_path)
            input(self.set.tip)
            return
        print(remark,"success 节点连接成功!")
        print(remark,"waiting 正在执行安装,请等待5-10分钟...")
        for cmd in self.set.cmdList:
            print(remark,cmd)
            console_in,console_out,console_error = ssh.exec_command(cmd)
            print(console_out.read().decode(),console_error.read().decode())
        ftp = Transport((host,int(port)))
        ftp.connect(username=self.set.username,password=password)
        sftp = SFTPClient.from_transport(ftp)
        sftp.put(mysql_config_path,self.set.server_user_config_path)
        ssh.exec_command("cd shadowsocksr && ./logrun.sh")
        ssh.exec_command(self.set.auto_start_cmd)
        ssh.exec_command(self.set.rc_chmod)
        remove(mysql_config_path)
        result = ssh.exec_command(self.set.ps_cmd)[1].read().decode()
        #print(result)
        if result:
            print(remark,"success 节点已启动,并加入开机启动...")
        else:
            print(remark,"FAIL 节点未运行,请登陆服务器查看！")
        ssh.close()
