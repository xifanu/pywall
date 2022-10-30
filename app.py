from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import re
import subprocess
import time
import os
import threading
import geoip2.database

app = Flask(__name__)

# windows 绝对路径：E:\pythonProject\pywall\db\my.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:\\pythonProject\\pywall\\db\\my.db'

# windows 相对路径：instance\mydb
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db'

# Linux 绝对路径：/usr/pywall/db/myy.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////usr/pywall/db/my.db'

db = SQLAlchemy(app)

class Clientip(db.Model):
    ip = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(200))

#IP 打码
def ipdama(strip):
    newstr = re.sub(r'(?!\d{1,3}\.\d{1,3}\.)\d', '*', strip)
    return newstr

@app.route('/')
def home():
    userip = request.remote_addr
    country = ipcountry(userip)
    clientips = Clientip.query.all()
    for clientip in clientips:
        ipxx = ipdama(clientip.ip)
        clientip.ip = ipxx
        if clientip.memo is None:
            clientip.memo = '未知'
    return render_template('index.html', clientips = clientips, userip = userip, country = country)

@app.route('/add', methods=['GET'])
def tohome():
    return redirect(url_for('home'))

@app.route('/add', methods=['POST'])
def create():
    userip = request.form['cadd']
    country = ipcountry(userip)
    new_ip_model = Clientip(ip=userip, memo = country)
    if re.match(r'^([1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])(\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])){3}$', userip):
        db_clientip = Clientip.query.get(userip)
        if db_clientip and len(db_clientip.ip) > 0:
            #已存在
            iptables_A(userip)
            return redirect(url_for('home'))
        else:
            #不存在
            iptables_A(userip)
            db.session.add(new_ip_model)
            db.session.commit()
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