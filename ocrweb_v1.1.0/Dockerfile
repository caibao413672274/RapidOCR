# 基于镜像基础
FROM python:3.9.5
Run apt-get update && apt-get install libgl1 -y
Run mkdir -p /data/ocrweb_v1.1.0
ADD ocrweb_v1.1.0 /data/ocrweb_v1.1.0

# 工作目录 /var/app
WORKDIR /data/ocrweb_v1.1.0
Run pip install -r requirements.txt -i https://pypi.douban.com/simple/
CMD ["python","main2.py"] 