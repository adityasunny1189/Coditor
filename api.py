from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import json
import time

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def api_call():
    if request.method == 'POST':
        
        # Adding multiple language support
        
        code = request.form['text_editor']
        language = request.form['language']
        input_value = request.form['input_value']
        print(f'language: {language}, input: {input_value}')
        d = {
            "code": f"{code}",
            "language": f'{language}',
            "input": f'{input_value}'
        }
        d1 = json.dumps(d)
        data = json.loads(d1)
        api_end_point_get_id = f'https://codersapi.herokuapp.com/api/codeall/'
        response_output = requests.post(api_end_point_get_id, json=data)
        print(f'Response Output: {response_output.text}')
        try:
            output = response_output.json()['output']
            error = response_output.json()['error']
            output = output.split('\n')
            return render_template('index.html', output=output, error=error)
        except AttributeError:
            return render_template('index.html', output=[], error='')
        
        # End Code
        
        
#         code = request.form['text_editor']
#         d = {
#             "code": f"{code}"
#         }
#         print(f'Code: {code}')
#         d1 = json.dumps(d)
#         data = json.loads(d1)
#         api_end_point_get_id = f'https://codersapi.herokuapp.com/api/coderun/'
#         response = requests.post(api_end_point_get_id, json=data)
#         json_response = response.json()
#         code_editor_id = json_response['id']
#         api_end_point_get_output = f'https://codersapi.herokuapp.com/api/output/'
#         di = {
#             "id": f"{code_editor_id}"
#         }
#         print(f'Id: {code_editor_id}')
#         time.sleep(5)
#         di1 = json.dumps(di)
#         data_id = json.loads(di1)
#         response_output = requests.post(api_end_point_get_output, json=data_id)
#         output = response_output.json()['output']
#         print(f'Output: {output}')
#         error = response_output.json()['error']
#         output = output.split('\n')
#         print(output)
#         return render_template('index.html', output=output, error=error)
    else:
        return render_template('index.html', output=[], error='')


if __name__ == '__main__':
    app.run()
