from flask import Flask, render_template, request, url_for, redirect
from flask_basicauth import BasicAuth
import re
import subprocess
import time
import os
import threading
import geoip2.database
import pickle
from gevent import pywsgi

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = '123456'

app.config['BASIC_AUTH_FORCE'] = False
basic_auth = BasicAuth(app)

# 初始化客户端的 ips 对象
ip_dict = {'8.8.8.8':'美国', '1.2.3.4':'美国'}
ips_dama = {}

ipv6_pattern = r'^(?=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$)(?:(?:25[0-5]|[12][0-4][0-9]|1[5-9][0-9]|[1-9]?[0-9])\.?){4}$|(?=^(?:[0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}$)(?![^:]*::.+::[^:]*$)(?:(?=.*::.*)|(?=\w+:\w+:\w+:\w+:\w+:\w+:\w+:\w+))(?:(?:^|:)(?:[0-9a-f]{4}|[1-9a-f][0-9a-f]{0,3})){0,8}(?:::(?:[0-9a-f]{1,4}(?:$|:)){0,6})?$'


# 写入文件 ip_dict
def wd_init_ips():
    with open('/usr/pywall/ip_dict','wb') as ips_file:
        pickle.dump(ip_dict, ips_file)
    ips_file.close()

# 写入文件 ip_dict
def wd_ips(cips):
    with open('/usr/pywall/ip_dict','wb') as ips_file:
        pickle.dump(cips, ips_file)
    ips_file.close()

# 读取文件 ip_dict
def read_ips():
    with open('/usr/pywall/ip_dict','rb') as ips_file:
        ips = pickle.load(ips_file)
        ips_file.close()
        return ips

# IP 打码
def ipdama(strip):
    newstr = re.sub(r'(?!\d{1,3}\.\d{1,3}\.)\d', '*', strip)
    return newstr

@app.route('/')
def home():
    ips_dama.clear()
    userip = request.remote_addr
    userip = userip.replace("::ffff:", "")
    country = ipcountry(userip)
    clientips_dict = read_ips()
    haveip = 0
    for cip, cipcountry in clientips_dict.items():
        if cip == userip:
            haveip = 1
            key_ip = '当前　' + userip
            ips_dama[key_ip] = '已添加'
    for cip, cipcountry in clientips_dict.items():
        ipxx = ipdama(cip)
        ips_dama[ipxx] = cipcountry
    return render_template('index.html', ips_dama = ips_dama, userip = userip, country = country)

@app.route('/add', methods=['GET'])
def tohome():
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def create():
    userip = request.form['cadd']
    country = ipcountry(userip)
    user_dict = {}
    user_dict[userip] = country
    clientips_dict = read_ips()
    if re.match(r'^([1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])(\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])){3}$', userip):
        # 判断 userip 是否存在于 clientips_dict
        if userip in clientips_dict:
            # 已存在
            iptables_A(userip)
            return redirect(url_for('home'))
        else:
            # 不存在
            iptables_A(userip)
            # 写入文件 ip_dict
            clientips_dict[userip] = country
            wd_ips(clientips_dict)
            return redirect(url_for('home'))
    if re.match(ipv6_pattern, userip):
        # 判断 userip 是否存在于 clientips_dict
        if userip in clientips_dict:
            # 已存在
            ip6tables_A(userip)
            return redirect(url_for('home'))
        else:
            # 不存在
            ip6tables_A(userip)
            # 写入文件 ip_dict
            clientips_dict[userip] = country
            wd_ips(clientips_dict)
            return redirect(url_for('home'))
    return redirect(url_for('home'))

@app.route('/initIP')
@basic_auth.required
def initIPRule():
    # 初始化 iptables rule
    start_runner()
    # 初始化 ips
    wd_init_ips()
    return redirect(url_for('home'))

def iptables_A( cip ):
    mysh = 'iptables -C INPUT -s %s -j ACCEPT' % cip
    ret1 = subprocess.Popen(mysh, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
    ret1.wait(3)
    out1, err1 = ret1.communicate()
    ipt_ret_info = '%s %s' % (out1, err1)
    if "Bad rule" in ipt_ret_info:
        ret2 = subprocess.Popen('iptables -A INPUT -s %s -j ACCEPT' % cip, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
        ret2.wait()


def ip6tables_A( cip ):
    mysh = 'ip6tables -C INPUT -s %s -j ACCEPT' % cip
    ret1 = subprocess.Popen(mysh, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
    ret1.wait(3)
    out1, err1 = ret1.communicate()
    ipt_ret_info = '%s %s' % (out1, err1)
    if "Bad rule" in ipt_ret_info:
        ret2 = subprocess.Popen('ip6tables -A INPUT -s %s -j ACCEPT' % cip, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
        ret2.wait()

def start_runner():
    print('....process iptables Rule....')
    init_iptables = 'bash /usr/pywall/ipt.sh'
    ret1 = subprocess.Popen(init_iptables, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
    ret1.wait(3)
    init_iptables = 'bash /usr/pywall/v6ipt.sh'
    ret1 = subprocess.Popen(init_iptables, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
    ret1.wait(3)

def ipcountry(userip):
    with geoip2.database.Reader('/usr/pywall/GeoLite2-Country.mmdb') as reader:
        try:
            response = reader.country(userip)
            return response.country.names['zh-CN']
        except:
            return '未知'

if __name__ == '__main__':
    subprocess.Popen('/bin/cp -rf /usr/pywall/blankip /usr/pywall/ip_dict', shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, encoding="utf-8")
    # start_runner()
    # app.run(debug=False,host='0.0.0.0',port=9950)
    server = pywsgi.WSGIServer(('::', 9950), app)
    server.serve_forever()
