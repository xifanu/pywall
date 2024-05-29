# What's the pywall ?

python 简易防火墙管理程序：pywall

默认端口：**9950**

默认地址：http://**IP**:**PORT**:9950

![Default index](screen/index.jpg) 


## Debian 10 11 安装 pywall 过程

[CentOS 7 教程点我](#CentOS-Stream-安装-pywall-过程)

Debian 10、11 安装过程：

### 处理防火墙

```
# 卸载 ufw，不使用ufw
ufw disable
apt-get remove ufw
apt-get purge ufw

# 安装或升级 iptables
apt-get install iptables -y
apt-get install iptables-persistent -y

# 如果有警告窗口，选择 Yes 即可
```

### 安装 python3

- python 要求 3.6+

```
apt update

apt upgrade -y

apt install python3-pip -y

pip3 install --upgrade pip

```

验证安装情况

```
python3 -V

pip3 -V
```


### 安装本程序 pywall

```
apt install git curl wget -y

cd /usr && git clone https://github.com/xifanu/pywall.git

cd /usr/pywall

chmod +x *.py
chmod +x *.sh
```

### 安装依赖

```
pip3 install -r requirements.txt
```

### 临时启动

```
# 临时启动验证，有 warning 警告没关系，程序正常运行即可。
python3 app.py
```

### 开机自启

注册 systemd 服务

```
cd /etc/systemd/system && vi pywall.service
```

复制粘贴以下内容

```
[Unit]
Description=My Pywall
After=syslog.target network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/pywall/app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

使其生效

```
systemctl daemon-reload

# 开机自启
systemctl enable pywall
# 启动 pywall
systemctl start pywall
# 停止 pywall
systemctl stop pywall
# 重启 pywall
systemctl restart pywall
# 查看 pywall 运行状态
systemctl status pywall
```

**附言**  
防火墙白名单规则初始化，执行： 
```
bash /usr/pywall/ipt.sh
```

如果执行出现报错，看下面： 
```
# 部分debian系统需要切换 iptables 版本，不然 netfilter-persistent save和netfilter-persistent reload执行报错
# 如果遇到 ipt.sh 执行报错，就需要切换 iptables 的版本
# iptables-nft和iptables-legacy这两个iptables使用了不同的内核模块
# 输入下面命令，准备切换 iptables 版本
update-alternatives --config iptables


# 屏幕打印出以下内容：
  Selection    Path                       Priority   Status
------------------------------------------------------------
* 0            /usr/sbin/iptables-nft      20        auto mode
  1            /usr/sbin/iptables-legacy   10        manual mode
  2            /usr/sbin/iptables-nft      20        manual mode

# 上面 星号 默认选择的 iptables-nft 版本，我们准备使用 iptables-legacy 版本。
# 找到 /usr/sbin/iptables-legacy 输入对应的数字： 1

# 设置成功后，屏幕输出以下内容：
# update-alternatives: using /usr/sbin/iptables-legacy to provide /usr/sbin/iptables (iptables) in manual mode
```


## CentOS Stream 安装 pywall 过程

（暂不支持 ipv6）

前提是：
- 网卡名称：eth0
- firewalld 已经安装并自启
- SSH 端口为 22

CentOS 7 安装 pywall 过程：

### 安装 python3

- 安装 python3 要求 3.6+

```
# 安装 python3
dnf install python3 -y

# 升级 pip3
pip3 install --upgrade pip
```

验证安装情况，python 的版本大于 3.6 即可

```
python3 -V

pip3 -V
```


### 安装本程序 pywall

```
dnf install git curl wget -y

cd /usr && git clone https://github.com/xifanu/pywall.git

cd /usr/pywall

chmod +x *.py
chmod +x *.sh
```

### 安装依赖

```
pip3 install -r requirements.txt
```

### 临时启动

```
# 临时启动验证
python3 centos_app.py
```

### 开机自启

注册 systemd 服务

```
cd /etc/systemd/system && vi pywall.service
```

复制粘贴以下内容

```
[Unit]
Description=My Pywall
After=syslog.target network.target nss-lookup.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/pywall/centos_app.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

使其生效

```
systemctl daemon-reload

# 开机自启
systemctl enable pywall
# 启动 pywall
systemctl start pywall
# 停止 pywall
systemctl stop pywall
# 重启 pywall
systemctl restart pywall
# 查看 pywall 运行状态
systemctl status pywall
```

### 初始化 firewalld 防火墙规则

以下命令根据实际情况灵活更改：

```
# 放行 cloudflare IP
firewall-cmd --permanent --zone=trusted --add-source=173.245.48.0/20
firewall-cmd --permanent --zone=trusted --add-source=103.21.244.0/22
firewall-cmd --permanent --zone=trusted --add-source=103.22.200.0/22
firewall-cmd --permanent --zone=trusted --add-source=103.31.4.0/22
firewall-cmd --permanent --zone=trusted --add-source=141.101.64.0/18
firewall-cmd --permanent --zone=trusted --add-source=108.162.192.0/18
firewall-cmd --permanent --zone=trusted --add-source=190.93.240.0/20
firewall-cmd --permanent --zone=trusted --add-source=188.114.96.0/20
firewall-cmd --permanent --zone=trusted --add-source=197.234.240.0/22
firewall-cmd --permanent --zone=trusted --add-source=198.41.128.0/17
firewall-cmd --permanent --zone=trusted --add-source=162.158.0.0/15
firewall-cmd --permanent --zone=trusted --add-source=104.16.0.0/13
firewall-cmd --permanent --zone=trusted --add-source=104.24.0.0/14
firewall-cmd --permanent --zone=trusted --add-source=172.64.0.0/13
firewall-cmd --permanent --zone=trusted --add-source=131.0.72.0/22
# docker
firewall-cmd --permanent --zone=trusted --add-source=172.17.0.1/24
firewall-cmd --permanent --zone=trusted --add-source=172.17.0.2/24
# 放行 22 SSH
firewall-cmd --permanent --add-port=22/tcp
# 放行 9950 Pywall
firewall-cmd --permanent --add-port=9950/tcp
firewall-cmd --reload
firewall-cmd --set-default-zone=drop
firewall-cmd --permanent --zone=drop --change-interface=eth0
firewall-cmd --reload
```
　
**其他说明**  

pywall 添加的防火墙规则为临时规则，系统重启后失效（上面的初始化防火墙规则始终生效，不会因为系统重启而失效）；

Linux 系统重启后，除了默认初始化的防火墙规则，通过 pywall 添加的规则会重置；

建议配置 crontab 定时重启，重启系统是为了清理添加的防火墙规则，时间长了放行的IP太多了，会不安全；

```
# 定时重启 每周五和周一，早晨5点重启
0 5 * * 5,1 reboot
```
