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