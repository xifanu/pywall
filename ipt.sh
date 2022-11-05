# Debian
iptables -F INPUT
# iptables -X INPUT
iptables -Z INPUT
iptables -A INPUT -p icmp -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp --dport 8000:9999 -j ACCEPT
iptables -A INPUT -p tcp --dport 44422 -j ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -s 172.16.0.0/12 -j ACCEPT
iptables -A INPUT -s 10.0.0.0/8 -j ACCEPT
iptables -A INPUT -s 192.168.0.0/16 -j ACCEPT
iptables -A INPUT -s 1.0.0.1 -j ACCEPT
iptables -A INPUT -s 1.0.0.2 -j ACCEPT
iptables -A INPUT -s 1.0.0.3 -j ACCEPT
# 禁止其他不匹配的规则访问本机
iptables -P INPUT DROP
#配置写入文件
modprobe ip_tables
iptables-save
netfilter-persistent save
netfilter-persistent reload
