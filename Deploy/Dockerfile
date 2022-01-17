FROM python:3.7-alpine
COPY . .
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip && \
    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -Ur requirements.txt
EXPOSE 1212
CMD ['python', '-Bu', 'app.py']