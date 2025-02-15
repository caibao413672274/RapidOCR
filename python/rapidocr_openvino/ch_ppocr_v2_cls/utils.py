# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import yaml
from openvino.runtime import Core


class OpenVINOInferSession(object):
    def __init__(self, config):
        ie = Core()
        model_onnx = ie.read_model(config['model_path'])
        compile_model = ie.compile_model(model=model_onnx, device_name='CPU')
        self.session = compile_model.create_infer_request()


def read_yaml(yaml_path):
    with open(yaml_path, 'rb') as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data


class ClsPostProcess(object):
    """ Convert between text-label and text-index """

    def __init__(self, label_list):
        super(ClsPostProcess, self).__init__()
        self.label_list = label_list

    def __call__(self, preds, label=None):
        pred_idxs = preds.argmax(axis=1)
        decode_out = [(self.label_list[idx], preds[i, idx])
                      for i, idx in enumerate(pred_idxs)]
        if label is None:
            return decode_out

        label = [(self.label_list[idx], 1.0) for idx in label]
        return decode_out, label