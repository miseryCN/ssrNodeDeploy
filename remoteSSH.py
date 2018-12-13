from paramiko import SSHClient,AutoAddPolicy,ssh_exception,Transport,SFTPClient
from settings import Settings
from queue import Queue
from json import dump
from threading import Thread
from os import remove,getcwd,path
from excelReader import readExcel



class RemoteSSH():
    def __init__(self):
        self.set = Settings()
        self.que = Queue()
        self.threadList = []
        self.workPath = getcwd() + "/"
        self.resultPath = self.workPath+self.set.result
        if path.exists(self.resultPath):
            remove(self.resultPath)
        if path.exists(self.workPath+"servers.xlsx"):
            self.servers_config_path = self.workPath + "servers.xlsx"
        elif path.exists(self.workPath+"servers.xls"):
            self.servers_config_path = self.workPath + "servers.xlsx"
        else:
            self.servers_config_path = ""


    def deploy(self):
        self.servers = readExcel(self.servers_config_path)
        if isinstance(self.servers,list):
            print("在配置文件中找到",len(self.servers),"个节点...")
            for server in self.servers:
                server = tuple(server)
                threadName = Thread(target=self.execute,args=server)
                self.threadList.append(threadName)
                threadName.start()
            Thread(target=self.daemon_check).start()
        else:
            print(self.set.config_not_found)
            host = input("节点地址:")
            port = int(input("节点ssh端口:"))
            password = input("节点root密码:")
            dbHost = input("数据库地址:")
            dbPassword = input("数据库密码:")
            dbName = input("数据库名:")
            nodeID = int(input("节点node_id:"))
            remark = "默认节点"

            self.execute(remark,host,port,password,dbHost,dbPassword,dbName,nodeID)



    def daemon_check(self):
        while True:
            threadAorD = []
            for thread in self.threadList:
                threadAorD.append(thread.isAlive())
            if True not in threadAorD and self.que.empty():
                result = self.read_result()
                input(result)
                return
            else:
                if not self.que.empty():
                    remark, host, info = self.que.get()
                    with open(self.resultPath,"a",encoding="utf-8") as f:
                        f.write(remark+" | "+host+": "+info+"\n")


    def check_config(self,*args):
        for arg in args[1:]:
            if arg == "":
                return False
        return True


    def execute(self,remark,host,port,password,dbHost,dbPassword,dbName,nodeID):
        if not self.check_config(remark,host,port,password,dbHost,dbPassword,dbName,nodeID):
            print(remark,self.set.error_info)
            self.que.put((remark,host,self.set.error_info))
            return

        print(remark,self.set.start)
        try:
            int(port),int(nodeID)
        except ValueError:
            print(remark,self.set.error_value)
            self.que.put((remark,host,self.set.error_value))
            return

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            print(remark,self.set.connect)
            ssh.connect(host,int(port),self.set.username,password)
        except ssh_exception.NoValidConnectionsError:
            print(remark,self.set.error_port)
            self.que.put((remark,host,self.set.error_port))
            return
        except ssh_exception.AuthenticationException:
            print(remark,self.set.error_pass)
            self.que.put((remark,host,self.set.error_pass))
            return
        except TimeoutError:
            print(remark,self.set.error_timeout)
            self.que.put((remark,host,self.set.error_timeout))
            return
        except:
            print(self.set.error_unknown)
            self.que.put((remark,host,self.set.error_unknown))
        print(remark,self.set.success_connect)
        print(remark,self.set.deploying)
        for cmd in self.set.cmdList:
            print(remark,cmd)
            print(self.set.wait_for_response)
            console_in,console_out,console_error = ssh.exec_command(cmd)
            print(console_out.read().decode(),console_error.read().decode())
        ftp = Transport((host,int(port)))
        ftp.connect(username=self.set.username,password=password)
        sftp = SFTPClient.from_transport(ftp)
        mysql_config_path = self.workPath+host+"_user_mysql.json"
        with open(mysql_config_path,"w",encoding="utf-8") as configFile:
            dump(self.set.generateUserMysqlFile(dbHost,dbPassword,dbName,nodeID),configFile)
        sftp.put(mysql_config_path,self.set.server_user_config_path)
        ssh.exec_command(self.set.log_run)
        ssh.exec_command(self.set.auto_start_cmd)
        ssh.exec_command(self.set.rc_chmod)
        remove(mysql_config_path)
        result = ssh.exec_command(self.set.ps_cmd)[1].read().decode()
        if result:
            print(remark,self.set.success_deploy)
            self.que.put((remark,host,self.set.success_deploy))
        else:
            print(remark,self.set.error_deploy)
            self.que.put((remark,host,self.set.error_deploy))
        ssh.close()


    def read_result(self):
        with open(self.resultPath,"r",encoding="utf-8") as f:
            text = f.read()
            return self.set.tip+text+self.set.end
