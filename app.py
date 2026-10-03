from flask import Flask, render_template, request
from tech_assistant_pro import ProTechAssistant
import os

app = Flask(__name__)
engine = ProTechAssistant()

@app.route('/', methods=['GET','POST'])
def index():
    result = None
    mock = None
    eval_result = None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'evaluate':
            code = request.form.get('code','')
            eval_result = engine.evaluate_code_pro(code)
        elif action == 'mock':
            company = request.form.get('company','Google')
            mock = engine.generate_mock(company, 3)
        else:
            topic = request.form.get('topic','arrays')
            diff = request.form.get('difficulty','medium')
            company = request.form.get('company','Google')
            prob = engine.get_problem(topic, diff)
            mock = {'company':company,'problems':[prob],'sd':engine.problems['system_design'][0]}

    return render_template('index.html', mock=mock, eval=eval_result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)