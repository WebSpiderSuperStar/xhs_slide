#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File         : main.py
# @Date         : 13-01-2022
# @Author       : Payne
# @Email        : wuzhipeng1289690157@gmail.com
# @Desc:
from src.bypass import rids
from execjs import compile
from fastapi import FastAPI

app = FastAPI()

file = open("src/device.js").read()


@app.get("/")
async def read_root():
    return {
        "Hello": "World"
    }


@app.get("/sm_captcha")
async def read_item(authorization: str):
    return {
        "authorization": authorization,
        "rid": rids(),
        "deviceId": compile(file).call("main"),
    }

# app = Flask(__name__)
#
# file = open("src/device.js").read()
#
#
# @app.route("/")
# def hello_world():
#     return '<h2 align="center">Welcome</h2>'
#
#
# @app.route("/sm_captcha", methods=["GET", "POST"])
# def sm_captcha():
#     return {
#         "authorization": request.form.get("authorization"),
#         "rid": rids(),
#         "deviceId": compile(file).call("main"),
#     }
#
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=1212)
