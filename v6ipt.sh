#!/bin/bash

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

source '/etc/os-release'

VERSION=$(echo "${VERSION}" | awk -F "[()]" '{print $2}')

ip6tables -F
# ip6tables -X
ip6tables -Z
ip6tables -I INPUT -p icmpv6 --icmpv6-type router-solicitation -m hl --hl-eq 255 -j ACCEPT
ip6tables -I INPUT -p icmpv6 --icmpv6-type router-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -I INPUT -p icmpv6 --icmpv6-type neighbor-solicitation -m hl --hl-eq 255 -j ACCEPT
ip6tables -I INPUT -p icmpv6 --icmpv6-type neighbor-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -I INPUT -p icmpv6 --icmpv6-type redirect -m hl --hl-eq 255 -j ACCEPT

ip6tables -A INPUT -p icmp -j ACCEPT
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT
ip6tables -A INPUT -p tcp --dport 80 -j ACCEPT
ip6tables -A INPUT -p tcp --dport 443 -j ACCEPT
ip6tables -A INPUT -p tcp --dport 8000:9999 -j ACCEPT
ip6tables -A INPUT -p udp --dport 8000:9999 -j ACCEPT
ip6tables -A INPUT -p tcp --dport 44422 -j ACCEPT
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
ip6tables -A INPUT -s ::/128  -j ACCEPT
ip6tables -A INPUT -s ::1/128  -j ACCEPT
ip6tables -A INPUT -s ::ffff:0:0/96  -j ACCEPT
ip6tables -A INPUT -s 100::/64  -j ACCEPT
ip6tables -A INPUT -s 64:ff9b::/96  -j ACCEPT
ip6tables -A INPUT -s 2001::/32  -j ACCEPT
ip6tables -A INPUT -s 2001:10::/28  -j ACCEPT
ip6tables -A INPUT -s 2001:20::/28  -j ACCEPT
ip6tables -A INPUT -s 2001:db8::/32  -j ACCEPT
ip6tables -A INPUT -s 2002::/16  -j ACCEPT
ip6tables -A INPUT -s fc00::/7  -j ACCEPT
ip6tables -A INPUT -s fe80::/10  -j ACCEPT
ip6tables -A INPUT -s ff00::/8  -j ACCEPT
ip6tables -A INPUT -s 2a09:bac5:636e:1173::1bd:a0 -j ACCEPT
ip6tables -A INPUT -s 2a02:7080::85b9:3a7d:a07d:1 -j ACCEPT

# 禁止其他不匹配的规则访问本机
ip6tables -P INPUT DROP

# 配置写入文件
if [[ "${ID}" == "centos" && ${VERSION_ID} -ge 7 ]]; then
    echo -e "${OK} ${GreenBG} 当前系统为 Centos ${VERSION_ID} ${VERSION} ${Font}"
    service ip6tables save
    systemctl restart ip6tables
elif [[ "${ID}" == "debian" && ${VERSION_ID} -ge 8 ]]; then
    echo -e "${OK} ${GreenBG} 当前系统为 Debian ${VERSION_ID} ${VERSION} ${Font}"
    ip6tables-save > /etc/iptables/rules.v6
elif [[ "${ID}" == "ubuntu" && $(echo "${VERSION_ID}" | cut -d '.' -f1) -ge 16 ]]; then
    echo -e "${OK} ${GreenBG} 当前系统为 Ubuntu ${VERSION_ID} ${UBUNTU_CODENAME} ${Font}"
    ip6tables-save > /etc/iptables/rules.v6
else
    echo -e "${Error} ${RedBG} 当前系统为 ${ID} ${VERSION_ID} 不在支持的系统列表内，安装中断 ${Font}"
    exit 1
fi
