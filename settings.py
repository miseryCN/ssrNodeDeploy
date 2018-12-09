

class Settings():
    def __init__(self):
        self.username = "root"
        self.server_user_config_path = "/root/shadowsocksr/usermysql.json"
        self.ps_cmd = "ps -ef | grep \"[s]erver.py m\""
        self.auto_start_cmd = "echo \"cd shadowsocksr && ./logrun.sh\" >> /etc/rc.local"
        self.rc_chmod = "chmod +x /etc/rc.d/rc.local"

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