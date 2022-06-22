import json
import logging
import os


def json_load(json_path, verbose=False):
    """
    读取json文件并返回内容字典
    """
    json_path = str(json_path)
    if isinstance(json_path, str):
        json_path = json_path.replace('\\', '/')
    try:
        assert os.path.exists(json_path)
    except Exception as e:
        if verbose:
            print('file not found !', e)
    try:
        with open(json_path, 'r') as fp:
            return json.load(fp)
    except Exception as e:
        if verbose:
            print('simple json load failed, try utf-8', e)
    try:
        with open(json_path, 'r', encoding='utf-8') as fp:
            return json.load(fp)
    except Exception as e:
        if verbose:
            print('utf-8 json load failed, try gbk', e)
    try:
        with open(json_path, 'r', encoding='gbk') as fp:
            return json.load(fp)
    except Exception as e:
        if verbose:
            print('gbk json load failed!', e)


def uniform_split_char(string, split_char='/'):
    """
    uniform the split char of a string
    """
    string = str(string)
    assert isinstance(string, str)
    return string.replace('\\', split_char).replace('/', split_char)


def dir_check(dir_path, verbose=False):
    """
    check if `dir_path` is a real directory path
    if dir not found, make one
    """

    dir_path = str(dir_path)
    if dir_path == '':
        return True
    assert isinstance(dir_path, str)
    dir_path = uniform_split_char(dir_path)
    if not os.path.isdir(dir_path):
        try:
            os.makedirs(dir_path)
            if verbose:
                print('dirs made: {}'.format(dir_path))
        except Exception as err:
            print(f'failed to make dir {dir_path}, error {err}')
        return False
    else:
        return True


def log_init(log_path, quiet=False, level=logging.INFO):
    """
    initialize logging 
    save the logging object in `config.Parameters.Logging_Object`

    after this operation,
    we could save logs with simple orders such as `logging.debug('test debug')` `logging.info('test info')` 
    logging level : debug < info < warning <error < critical

    Loger_printer.vvd_logging('test')
    """
    log_path = str(log_path)
    dir_name = os.path.dirname(log_path)

    dir_check(dir_name)
    log_file_path = log_path

    if os.path.exists(log_file_path):
        # open log file as  mode of append
        open_type = 'a'
    else:
        # open log file as  mode of write
        open_type = 'w'

    # basicConfig 无法解决中文乱码的问题, 封存相关代码
    # 据说 Python 3.9 之后会加入basicConfig() 的encoding和errors关键字配置
    # logging.basicConfig(
    #     # 日志级别,logging.DEBUG,logging.ERROR
    #     level=level,
    #     # 日志格式: 时间、   日志信息
    #     format='%(asctime)s: %(message)s',
    #     # 打印日志的时间
    #     datefmt='%Y-%m-%d %H:%M:%S',
    #     # 日志文件存放的目录（目录必须存在）及日志文件名
    #     filename=log_file_path,
    #     # 打开日志文件的方式
    #     filemode=open_type
    # )
    # logging.StreamHandler()

    # create logger obj
    logger = logging.getLogger()
    # set log level
    logger.setLevel(level)
    # file handler
    handler = logging.FileHandler(log_file_path, mode=open_type, encoding='utf-8')
    handler.setFormatter(logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s"))

    for old_handler in logger.handlers[::-1]:
        old_handler.stream.close()
        logger.removeHandler(old_handler)

    logger.addHandler(handler)

    if quiet:
        return Loger_printer(logger).vvd_logging_quiet
    else:
        return Loger_printer(logger).vvd_logging


class Loger_printer():
    """
    日志打印类
    会在控制台与日志同时打印信息    
    """

    def __init__(self, logger):
        self.logger = logger
        self.logger_dict = {
            logging.DEBUG: self.logger.debug,
            logging.INFO: self.logger.info,
            logging.WARNING: self.logger.warning,
            logging.ERROR: self.logger.error,
            logging.CRITICAL: self.logger.critical
        }
        self.closed = False

    def get_logger_func(self, level):
        if level in self.logger_dict:
            return self.logger_dict[level]
        else:
            raise RuntimeError(f"unknown level {level}, {self.logger_dict}")

    def vvd_logging(self, *message, level=logging.INFO, close_logger=False):
        if not self.closed:
            log_func = self.get_logger_func(level)
            if message is not None:
                for message_str in message:
                    print(message_str)
                    log_func(message_str)
            if close_logger:
                for handler in self.logger.handlers:
                    handler.close()
        else:
            print('logger has been closed')

    def vvd_logging_quiet(self, *message, level=logging.INFO, close_logger=False):
        if not self.closed:
            log_func = self.get_logger_func(level)
            if message is not None:
                for message_str in message:
                    log_func(message_str)
            if close_logger:
                for handler in self.logger.handlers:
                    handler.close()
        else:
            print('logger has been closed')
