FROM python:3.7-slim
WORKDIR /app
COPY ./requirements.txt .
RUN  ln -sf /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/timezone && \
     pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3", "run.py"]
