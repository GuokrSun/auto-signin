import json
import time
import re
import requests

from modules import tieba

# 初始化
def main():
    cookies = ''
    tieba.init(cookies)

if __name__ == '__main__':
    main()
