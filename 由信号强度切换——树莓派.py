# 扫描附近的wifi并输出
import sys
import time
import os
from pywifi import Profile, PyWiFi, const


# 扫描当前WiFi信号
def test_scan():
    wifi = PyWiFi()  # 创建一个无线对象
    iface = wifi.interfaces()[0]  # 取一个无限网卡
    iface.scan()  # 扫描s
    # (必不可少)这个sleep时间必须有，不知道为啥。
    time.sleep(0.5)
    wifi_information = {'ABCD': [-200, 123456789],
                        'hello_world': [-200, 850898840]}
    result = iface.scan_results()
    for i in range(len(result)):
        if result[i].ssid in wifi_information.keys():
            wifi_information[result[i].ssid] = [result[i].signal,
                                                wifi_information[result[i].ssid][1]]
    # time.sleep(1)
    return wifi_information


# 对信号强度进行排序
def sort_Strength():
    wifi_information = test_scan()
    for key, value in wifi_information.items():
        wifi_information_sorted = sorted(wifi_information.items(),
                                         key=lambda wifi_information: wifi_information[1],
                                         reverse=True)
    wifi_Name = wifi_information_sorted[0][0]  # 取出第一个元组中的key值
    wifi_Password = wifi_information_sorted[0][1][1]
    # print(wifi_Name)
    # print(wifi_information)
    # print(wifi_information_sorted)
    # time.sleep(1)
    return [wifi_Name, wifi_Password, wifi_information_sorted]


# 检查当前WiFi信号通断状态
def check_ping(ip='202.108.22.5', count=1, timeout=1000):
    for i in range(3):
        cmd = 'ping -n %d -w %d %s >NUL' % (count, timeout, ip)
        res = os.system(cmd)
        res += res
    return 'ok' if res == 0 else 'failed'
    time.sleep(10)


# 连接wifi
def connect_wifi(wifi_name, wifi_password):
    wifi = PyWiFi()  # 创建一个无限对象
    ifaces = wifi.interfaces()[0]  # 取一个无限网卡
    # print(ifaces.name())  # 输出无线网卡名称
    ifaces.disconnect()  # 断开网卡连接
    # time.sleep(1)  # 缓冲3秒
    profile_info = Profile()  # 配置文件
    profile_info.ssid = wifi_name  # wifi名称
    profile_info.auth = const.AUTH_ALG_OPEN  # 需要密码
    profile_info.akm.append(const.AKM_TYPE_WPA2PSK)  # 加密类型
    profile_info.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
    profile_info.key = wifi_password
    ifaces.remove_all_network_profiles()  # 删除其他配置文件
    tmp_profile = ifaces.add_network_profile(profile_info)  # 加载配置文件
    ifaces.connect(tmp_profile)  # 连接
    time.sleep(2)  # (必不可少)尝试2秒能否成功连接
    isok = True
    if ifaces.status() == const.IFACE_CONNECTED:
        print("成功切换连接为wifi: %s" % wifi_name)

    else:
        print("wifi: %s 连接失败" % wifi_name)
    # time.sleep(2)
    return isok


def main():
    while True:
        networkStatus = check_ping()
        list_wifi_information = sort_Strength()
        wifi_information = test_scan()
        wifi_information_sorted = list_wifi_information[2]
        if networkStatus == 'ok':
            print('网络正常' + str(time.time()))
            wifi_information_sorted_again = sorted(wifi_information.items(),
                                                   key=lambda wifi_information: wifi_information[1],
                                                   reverse=True)
            # 由于wifi_information_sorted已经在前面itmes()一次了，所以这里直接用。
            # wifi_information_sorted_again 是前面同样的词典以元组格式输出。
            # wifi_information_sorted_again[1][1][0]是信号强度
            # wifi_information_sorted_again[0][1]是[singal,password]列表
            # wifi_information_sorted_again[0][0]是wifi名称
            # wifi_information_sorted_again[0][1][1]是wif密码
            if wifi_information_sorted_again[1][1][0] - wifi_information_sorted[1][1][0] > 10:
                # 这里可能需要改一下，不知道为啥也照样能连接。
                print("信号切换")
                connect_wifi(wifi_information_sorted_again[0][0],
                             wifi_information_sorted_again[0][1][1])
        else:
            print("网络无信号")
            connect_wifi(list_wifi_information[0], list_wifi_information[1])
            # time.sleep(0.5)


if __name__ == "__main__":
    main()
