import time
import subprocess
import re


def get_date_str():
    str_time = time.localtime(time.time())
    year = str_time.tm_year
    mounth = str_time.tm_mon
    day = str_time.tm_mday

    date_str = f"{year}-{mounth}-{day}"
    return date_str


def ipv4_func(card='ppp0'):  # 局域网ipv4
    ret = subprocess.getstatusoutput(f'ifconfig')[1]
    ret = ret.split(card, 1)[1].split('inet ', 1)[1].strip().split(' ', 1)[0]
    ret = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', ret).group()
    return ret


if __name__ == "__main__":
    print(ipv4_func('en0'))
