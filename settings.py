

class Settings():
    def __init__(self):
        self.username = "root"
        self.result = "result.txt"
        self.wait_for_response = "命令已发送,等待节点服务器反馈结果..."
        self.error_unknown = "ERROR 未知错误"
        self.server_user_config_path = "/root/shadowsocksr/usermysql.json"
        self.ps_cmd = "ps -ef | grep \"[s]erver.py m\""
        self.auto_start_cmd = "echo \"cd shadowsocksr && ./logrun.sh\" >> /etc/rc.local"
        self.rc_chmod = "chmod +x /etc/rc.d/rc.local"
        self.start = "start 开始部署..."
        self.error_info = "ERROR 节点信息不全!"
        self.error_value = "ERROR ssh端口或node_id只能是数字!"
        self.connect = "waiting 正在连接节点..."
        self.error_port = "ERROR 错误的端口或地址!"
        self.error_pass = "ERROR 身份认证失败!"
        self.error_timeout = "ERROR 节点连接超时!"
        self.success_connect = "success 节点连接成功!"
        self.deploying = "waiting 正在执行安装,请等待5-10分钟..."
        self.success_deploy = "success 节点已启动,并加入开机启动..."
        self.error_deploy = "FAIL 节点未运行,请登陆服务器查看！"
        self.config_not_found = "ERROR 未在当前目录下找到配置文件","servers.csv","请手动输入配置信息..."

        self.tip = "\n\n\n程序运行结束,结果如下(已写入result.txt):\n\n"
        self.end = "\n按回车结束..."
        self.log_run = "cd shadowsocksr && ./logrun.sh"
        self.cmdList = [
            "yum -y install wget git vim",
            "ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime",
            "yum -y groupinstall \"Development Tools\"",
            "firewall-cmd --zone=public --add-port=10000-30000/tcp --permanent",
            "firewall-cmd --zone=public --add-port=10000-30000/udp --permanent",
            "firewall-cmd --reload",
            "wget https://github.com/jedisct1/libsodium/releases/download/1.0.16/libsodium-1.0.16.tar.gz",
            "tar xf libsodium-1.0.16.tar.gz",
            "cd /root/libsodium-1.0.16 && ./configure && make -j2 && make install && ldconfig",
            "echo /usr/local/lib > /etc/ld.so.conf.d/usr_local_lib.conf",
            "git clone https://github.com/miseryCN/shadowsocksr.git",
            "cd /root/shadowsocksr && ./initcfg.sh"

        ]



    def generateUserMysqlFile(self,dbHost,dbPassword,dbName,nodeID):
        UserMysqlConfigContent = {
            "host": dbHost,
            "port": 3306,
            "user": "root",
            "password": dbPassword,
            "db": dbName,
            "node_id": int(nodeID),
            "transfer_mul": 1.0,
            "ssl_enable": 0,
            "ssl_ca": "",
            "ssl_cert": "",
            "ssl_key": ""
        }
        return UserMysqlConfigContent