# Copyright 2020 IBM Corporation
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

from flask import Blueprint, render_template
import json
from qpylib import qpylib
import time
from datetime import datetime, timedelta

# pylint: disable=invalid-name
viewsbp = Blueprint('views', __name__, url_prefix='/')


@viewsbp.route('/getOffenses')
def getOffenses():
    try:
        api_1 = '/api/siem/offense_closing_reasons'
        headers = {'content-type' :  'application/json'}
        response_closing = qpylib.REST('GET', api_1, headers=headers)
        closing_reason = response_closing.json()
        yday = datetime.strftime(datetime.now() - timedelta(1), '%d.%m.%Y %H:%M:%S,%f')
        date_obj = datetime.strptime (yday, '%d.%m.%Y %H:%M:%S,%f')
        milliseconds = date_obj.timestamp() * 1000
        time_mil = round(milliseconds)
        api_2 = 'api/siem/offenses?fields=id%2C%20closing_reason_id&filter=status%3D%22CLOSED%22%20%20and%20close_time%20%3E%20' + str(time_mil)
        response_offenses = qpylib.REST('GET', api_2, headers=headers)
        offenses = response_offenses.json()   
        result = [] 
        for reason in closing_reason:
            calculo = {}
            calculo['id']=reason['id']
            calculo['text']=reason['text']
            calculo['count'] = 0
            for ofensa in offenses:
                if ofensa['closing_reason_id'] == reason['id']:
                    calculo['count'] = calculo['count'] + 1
            result.append(calculo)
    except Exception as e:
        qpylib.log(str(e), level='ERROR')
    return json.dumps(result)
