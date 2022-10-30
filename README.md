# pywall


![Default index](screen/index.jpg) 


python3 iptables 防火墙管理

- python 要求 3.6+

下面以 Debian 10、11 举例。

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

## 安装本程序 pyfw

```
mkdir /usr/pywall && cd /usr/pywall
```

```
# 直接ftp传输代码
# 代码位置及层级示例： /usr/pywall/app.py
```

## 安装依赖

```
chmod +x *.py
chmod +x *.sh
```

```
pip3 install -r requirements.txt
```

## 临时启动

```
python3 app.py
```

## 开机自启

注册 systemd 服务

```
cd /etc/systemd/system

vi pywall.service
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

systemctl enable pywall
```