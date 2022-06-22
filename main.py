from lib import DDNS, get_date_str, ipv4_func, log_init, json_load
import time
from pathlib import Path


if __name__ == "__main__":
    # 日志文件
    logger_file = Path('log') / (get_date_str() + '.log')
    print(logger_file)
    logger = log_init(logger_file)
    logger("*" * 60)
    logger("*" * 18 + '  Baidu DDNS start !!!  ' + "*" * 18)
    logger("*" * 60)

    # 循环更新
    ddns_obj = DDNS.from_cofig('assets/my_config.json', ipv4_func)  # 配置文件
    while True:
        domain_info_L = json_load('assets/domain.json')  # 更新的域名信息
        for domain_info in domain_info_L:
            try:
                successful = ddns_obj.SET(
                    domain=domain_info['name'],
                    ip_type=domain_info['ip_type'],
                    ttl=domain_info['ttl'],
                    logger=logger,
                )
                if successful:
                    logger('='*5 + f"Above domain name: {domain_info['name']}")
            except Exception as e:
                logger(f"ddns_obj SET failed: {e}")
        time.sleep(15)  # 检测间隔时间，秒
