# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import base64
import json
from wsgiref.simple_server import make_server

import cv2
import numpy as np
from flask import Flask, render_template, request

from task import detect_recognize

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024


@app.route('/test/2cbb34c23f99b5a86e50289f54d254f4')
def bbysocrweb():
    return render_template('bbysocrweb.html')


@app.route('/')
def index():
    return 'welcome to rapidocr'

@app.route('/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        result = {'code':0, 'msg':''}
        try:
            url_get = request.get_json()
            #img_str = str(url_get).split(',')[1]
            img_str = url_get.get('file')
            isapi=url_get.get('api')
            token=url_get.get('token')
            
            #md5(bbysocrapi)=2b7ca9081a2305ca47a656b1ff3bf634 用于api
            #md5(bbysocrweb)=2cbb34c23f99b5a86e50289f54d254f4 用于web
            if isapi is None:
                isapi=False

            if isapi==False:
                img_str = url_get.get('file').split(',')[1]
                if token !='2cbb34c23f99b5a86e50289f54d254f4':
                    result['msg']='Forbidden'
                    return json.dumps(result)
            else:
                if token !='2b7ca9081a2305ca47a656b1ff3bf634':
                    result['msg']='Forbidden'
                    return json.dumps(result)
            
            image = base64.b64decode(img_str)
            nparr = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image.ndim == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

            if isapi:
                rec_res_data = detect_recognize(image, is_api=True)
                result['code']=1
                result['data']=rec_res_data
                return json.dumps(result,indent=2,ensure_ascii=False)
            else:
                img, elapse, elapse_part, rec_res_data = detect_recognize(image)
                result['code']=1
                result['data']={'image': img,
                            'total_elapse': f'{elapse:.4f}',
                            'elapse_part': elapse_part,
                            'rec_res': rec_res_data}
                return json.dumps(result,indent=2,ensure_ascii=False)
        except Exception as e:
            result['code']=-1
            result['msg']=traceback.format_exc()
            return json.dumps(result)


if __name__ == '__main__':
    ip = '0.0.0.0'
    ip_port = 9003

    server = make_server(ip, ip_port, app)
    server.serve_forever()
