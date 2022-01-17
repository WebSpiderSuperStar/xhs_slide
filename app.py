#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File         : app.py
# @Date         : 13-01-2022
# @Author       : Payne
# @Email        : wuzhipeng1289690157@gmail.com
# @Desc:
import json

from src.bypass import applet_bypass

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h2 align="center"> Welcome</h2>'


@app.route('/sm_captcha', methods=['POST'])
def sm_captcha():
    results = {
        "authorization": request.form.get('authorization'),
        "verify": applet_bypass(authorization=request.form.get('authorization')),
    }
    return json.dumps(results, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=1212)