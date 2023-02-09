from flask import Flask, render_template, request, url_for, redirect
import re
import subprocess
import time
import os
import threading
import geoip2.database
import pickle


app = Flask(__name__)

# 初始化客户端的 ips 对象
ip_dict = {'8.8.8.8':'美国', '1.2.3.4':'美国'}
ips_dama = {}

# 写入文件 ip_dict
def wd_ips():
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
    country = ipcountry(userip)
    clientips_dict = read_ips()
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
    return redirect(url_for('home'))

@app.route('/initIPRule')
def initIPRule():
    start_runner()
    clientips = Clientip.query.all()
    for clientip in clientips:
        db.session.delete(clientip);
    db.session.commit()
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

def start_runner():
    print('....process iptables Rule....')
    init_iptables = 'bash /usr/pywall/ipt.sh'
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
    # start_runner()
    app.run(debug=False,host='0.0.0.0',port=9950)