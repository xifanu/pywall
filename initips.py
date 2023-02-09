import pickle
import os


# 初始化客户端的 ips 对象
ip_dict = {'8.8.8.8':'美国', '1.2.3.4':'美国'}

# 写入文件 ip_dict
def wd_ips():
    with open('./ip_dict','wb') as ips_file:
        pickle.dump(ip_dict, ips_file)
    ips_file.close()

# 读取文件 ip_dict
def read_ips():
    with open('./ip_dict','rb') as ips_file:
        ips = pickle.load(ips_file)
        ips_file.close()
        return ips
    

wd_ips()
print(read_ips())
