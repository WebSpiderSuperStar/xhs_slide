#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File         : bypass.py
# @Date         : 11-01-2022
# @Author       : Payne
# @Email        : wuzhipeng1289690157@gmail.com
# @Desc:
import random
from typing import AnyStr, List
from src.xhs_slide import rids
import requests
import json
from loguru import logger
from fire import Fire
from execjs import compile
from os.path import dirname, abspath, join


js_path = join(dirname(__file__), 'device.js')

js_res = open(js_path, encoding="utf8").read()

# for i in range(10):
#     print(compile(js_res).call("main"))


def applet_bypass(
        authorization: AnyStr = random.choice([
            "wxmp.25a1d7d4-5ced-4b1a-b037-a99be272c99c",
            "wxmp.8857a74d-14dc-4ed6-b157-3c8fb7df16de",
            "wxmp.03e2fd17-c98e-4fbc-bfa9-1f028f96d642",
            "wxmp.a009620c-7b90-4674-8418-19ef76334816",
            "wxmp.df473d8f-dbb0-43dc-8688-4b0eefc201eb",
        ]),
) -> None:
    url = "https://www.xiaohongshu.com/fe_api/burdock/weixin/v2/shield/captchaV2"
    logger.info(f"\t\n\tauthorizations: {authorization}\t\n \t")
    headers = {
        "Host": "www.xiaohongshu.com",
        "charset": "utf-8",
        "content-type": "application/json",
        "x-sign": "X013b36ebf3a70cf8a82051e3f246ab19",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20210501 Mobile Safari/537.36 MMWEBID/5616 MicroMessenger/8.0.6.1900(0x28000635) Process/appbrand0 WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",
        "authorization": authorization,
        "device-fingerprint": compile(js_res).call("main"),
        "Referer": "https://servicewechat.com/wxb296433268a1c654/60/page-frame.html",
    }
    dat = {"rid": rids(), "status": 1, "callFrom": "wxMiniProgram"}
    response = requests.post(url, headers=headers, data=json.dumps(dat))
    logger.info(response.json())
    return response.json()


if __name__ == "__main__":
    # print(dirname(__file__))
    Fire(applet_bypass)
