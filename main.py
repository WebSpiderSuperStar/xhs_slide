#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File         : main.py
# @Date         : 19-01-2022
# @Author       : Payne
# @Email        : wuzhipeng1289690157@gmail.com
# @Desc:

import json

import fire

from src.bypass import applet_bypass


def sm_captcha(authorization):
    results = {
        "authorization": authorization,
        "verify": applet_bypass(authorization=authorization),
    }
    return json.dumps(results, ensure_ascii=False)


if __name__ == '__main__':
    fire.Fire(sm_captcha)