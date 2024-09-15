import os
import subprocess
import requests
import re
#0可以 1不行
#JP_NF
#HK_PV

def get_uuid():
    if not os.path.exists('uuid.txt'):
        uuid = input("请输入您的UUID: ")
        with open('uuid.txt', 'w') as f:
            f.write(uuid)
    else:
        with open('uuid.txt', 'r') as f:
            uuid = f.read().strip()
    return uuid


def get_region():
    print("请选择地区代码:")
    print("日本 -- JP")
    print("香港 -- HK")
    print("新加坡 -- SG")
    print("台湾 -- TW")
    print("美国 -- US")
    print("本地和国际流媒体不建议混用 请按需使用 否则不保证100%解锁")
    region = input("请输入地区代码: ")
    return region



def send_request(uuid, region):
    url = f"http://38.207.160.142:8080?uuid={uuid}&region={region}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('value')
    else:
        print("请求失败:", response.json())
        return None

# 地区代码到中文名称的映射
region_map = {
    "JP": "日本",
    "HK": "香港",
    "SG": "新加坡",
    "TW": "台湾",
    "US": "美国",
    "HAMI": "Hami Video:				[32mYes[0m",
    "BAHAMUT": "Bahamut Anime:				[32mYes (Region: TW)[0m",
    "GPT": "ChatGPT:				[32mYes[0m"
}

def nf_test(region_name):
    for _ in range(10):
        if media == "GL":
            print("0")
            result = os.popen("./nf")
            result = result.read()
            print(result)
            if "您的出口IP完整解锁Netflix，支持非自制剧的观看" in result and f"所识别的IP地域信息：{region_name}" in result:
                print("done")
                return 0

def big_test():
    process = subprocess.Popen(
        'echo 1 | bash check.sh -M 4',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    output = stdout
    return output

def switch(media, ip, file_path='/etc/dnsmasq.d/custom_netflix.conf'):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 用于匹配IPv4地址的正则表达式
    ipv4_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

    # 修改文件内容
    with open(file_path, 'w') as file:
        for line in lines:
            if media in line:
                # 替换匹配行中的IPv4地址为新的IP地址
                modified_line = ipv4_pattern.sub(ip, line)
                file.write(modified_line)
            else:
                file.write(line)
    os.system('systemctl stop dnsmasq')
    os.system('systemctl start dnsmasq')
    print("work_done")




uuid = get_uuid()

#nf
while True:
    region = get_region()
    media = 'NF'
    data = f"{region}_{media}"
    dns_ip = send_request(uuid, data)
    region_name = region_map.get(region, "未知地区")
    switch('netflix.com', dns_ip)
    result = nf_test(region_name)
    if result == 0:
        break

#pv
while True:
    region = get_region()
    media = 'PV'
    data = f"{region}_{media}"
    dns_ip = send_request(uuid, data)
    region_name = region_map.get(region, "未知地区")
    switch('prime', dns_ip)
    switch('amazon', dns_ip)
    result = big_test()
    if f"Amazon Prime Video:			[32mYes (Region: {region})[0m" in result:
        break

#gpt
while True:
    data = 'GPT'
    dns_ip = send_request(uuid, data)
    region_name = region_map.get(region, "未知地区")
    switch('openai.com', dns_ip)
    result = big_test()
    if "ChatGPT:				[32mYes[0m" in result:
        break

#动画疯
while True:
    data = 'BAHAMUT'
    dns_ip = send_request(uuid, data)
    region_name = region_map.get(region, "未知地区")
    switch('openai.com', dns_ip)
    result = big_test()
    if "Bahamut Anime:				[32mYes (Region: TW)[0m" in result:
        break

#HAMI
while True:
    data = 'HAMI'
    dns_ip = send_request(uuid, data)
    region_name = region_map.get(region, "未知地区")
    switch('openai.com', dns_ip)
    result = big_test()
    if "Hami Video:				[32mYes[0m" in result:
        break
