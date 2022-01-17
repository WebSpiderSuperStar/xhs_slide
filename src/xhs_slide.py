#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File         : xhs_slide.py
# @Date         : 13-01-2022
# @Author       : Payne
# @Email        : wuzhipeng1289690157@gmail.com
# @Desc:
import cv2
import requests
from Crypto.Cipher import DES
import re, json, time, base64
from loguru import logger


def scrape(req_method, req_uri, req_header, req_params, req_dat) -> requests.Response:
    """请求方法
   :param req_method:
   :param req_uri:
   :param req_header:
   :param req_params:
   :param req_dat:
   :return: requests.Response
   """
    try:
        logger.info(f"scraping url: {req_uri}")
        resp = requests.request(
            method=str(req_method).upper(),
            url=req_uri,
            headers=req_header,
            params=req_params,
            data=req_dat
        )
        if resp.status_code == 200:
            return resp
        logger.error(f"An error occurred while crawling, status code: {resp.status_code}, req_uri: {req_uri}")
    except requests.RequestException as e:
        logger.error(
            f"A request exception occurred while crawling, status code: {resp.status_code}, req_uri: {req_uri}"
        )


def encrypt(key, text):
    """DES 加密
    :param key: 密钥, 长度必须为 16(AES-128)、24(AES-192)、32(AES-256) Bytes 长度
    :param text: 密文
    :return:
    """
    encrypter = DES.new(key.encode(), DES.MODE_ECB)
    length = 8
    count = len(text)
    if count < length:
        add = (length - count)
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)
    ciphertext = encrypter.encrypt(text.encode())
    return base64.b64encode(ciphertext)


class ShuMei:
    '''
    响应体riskLevel为pass即验证成功
    '''

    def __init__(self, deviceId):
        self.deviceId = deviceId
        self.register_url = "https://captcha.fengkongcloud.com/ca/v1/register"
        self.fverify_url = "https://captcha.fengkongcloud.com/ca/v2/fverify"
        self.img_url = "https://castatic.fengkongcloud.com"
        self.organization = "eR46sBuqF0fdw7KWFLYa"
        self.rid = ''
        self.timestamp = str(int(time.time() * 1000))
        self.js_url = self.captcha_js()[0]
        self.js_ver = self.captcha_js()[1]
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'captcha.fengkongcloud.com',
            'Referer': 'https://www.ishumei.com/trial/captcha.html',
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'script',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        }
        self.img_paths = 'bg.png', 'fg.png'

    def get_register_data(self):
        data = {
            'sdkver': '1.1.3',
            'channel': 'Lite',
            'rversion': '1.0.3',
            'model': 'slide',
            'lang': 'zh-cn',
            'data': '{"os":"android","sdkver":"1.2.4","deviceId":"' + self.deviceId + '"}',
            'appId': 'default',
            'callback': f"sm_{self.timestamp}",
            'organization': self.organization,
        }
        # res = requests.get(url=self.register_url,
        #                    headers=self.header, params=data)
        res = scrape(
            req_method='get',
            req_uri=self.register_url,
            req_header=self.header,
            req_params=data,
            req_dat={}
        )
        register_data = re.search("sm_\d+\((.*?)\)", res.text).group(1)
        return json.loads(register_data)['detail']

    def save_img(self, img_urls):
        for i in range(2):
            res = scrape('get', self.img_url + img_urls[i], {}, {}, {})
            with open(self.img_paths[i], 'wb', ) as f_wb:
                f_wb.write(res.content)

    def img_distance(self):
        """
        获取缺口距离
        :return:    缺口距离
        """
        target = self.img_paths[0]
        template = self.img_paths[1]
        target_rgb = cv2.imread(target)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(template, 0)
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        distance = value[3][0] + 7
        return int(distance / 2)

    def captcha_js(self):
        """
        获取js版本
        :return:  js_url  protocolc数值
        """
        url = f"https://captcha.fengkongcloud.com/ca/v1/conf?lang=zh-cn&organization={self.organization}&channel=GooglePlay&appId=default&callback=sm_{str(int(time.time()) * 1000)}&rversion=1.0.1&sdkver=1.1.3&model=slide"
        # res = requests.get(url).text
        res = scrape(req_method='get', req_uri=url, req_header={}, req_dat={}, req_params={})
        js_ver = re.search('-(\d+)/captcha-sdk', res.text).group(1)
        js_url = "https://castatic.fengkongcloud.com" + \
                 re.search('"js":"(.*?)"}', res.text).group(1)
        return js_url, js_ver

    def generate_params(self):
        data = self.get_register_data()
        img_urls = [data['bg'], data['fg']]
        self.save_img(img_urls)
        self.rid = data['rid']
        organization = self.organization
        ostype = 'web'
        callback = f'sm_{int((time.time()) * 1000)}'
        sdkver = '1.1.3'
        rversion = '1.0.1'
        distance = self.img_distance()
        params = {
            'dl': encrypt("2575232a", str(distance / 310)).decode('utf-8'),
            'rid': self.rid,
            'organization': organization,
            'ostype': ostype,
            'callback': callback,
            'sdkver': sdkver,
            'rversion': rversion,
            'atc.os': "android",
            'protocol': self.js_ver
        }
        return params

    def passed(self):
        err_num = 0
        while 1:
            err_num += 1
            params = self.generate_params()
            res = scrape(
                req_method='get',
                req_uri=self.fverify_url,
                req_header=self.header,
                req_params=params,
                req_dat={}
            )
            if 'PASS' in res.text:
                return self.rid
            if err_num > 10:
                print("err_num > 10")
                break


def rids(device=""):
    shumei = ShuMei(deviceId=device)
    rid = shumei.passed()
    return rid


if __name__ == '__main__':
    print(rids())