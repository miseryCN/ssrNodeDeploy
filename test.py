import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("13.229.134.149",22,"root","Yuxiaowei.1994")
b= ssh.exec_command("ps -ef | grep \"[s]erver.py m\"")[1]
d = b.read().decode()
if not d:
    print("没找到")
else:
    print("找到啦")