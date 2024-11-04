from flask import Flask, request, jsonify
import sys
sys.path.append("../Eval") 
from GradingOnly import load_and_predict
from GradingAgent import getEval

app = Flask(__name__)

@app.route('/process_text', methods=['POST'])
def process_text():
    # 获取 JSON 数据
    data = request.get_json()
    
    # 检查请求中是否有 'text' 字段
    if 'text' not in data:
        return jsonify({'error': 'Missing "text" field in request'}), 400
    
    text = data['text']

    overall_score = load_and_predict(text, "../Models/y_overall_model.joblib")
    recommendation_score = load_and_predict(text, "../Models/y_recommend_hiring_model.joblib")
    structured_answers_score = load_and_predict(text, "../Models/y_structured_answers_model.joblib")

    evaluation = getEval(text, overall_score, recommendation_score, structured_answers_score)
    # # # 在此处进行文字处理逻辑
    # # response_text = f"Received text: {text}"
    # # 返回 JSON 响应
    return jsonify({'evaluation': evaluation, 'overall_score':overall_score, 'recommendation_score':recommendation_score, 'structured_answers_score':structured_answers_score})
    
if __name__ == '__main__':
    app.run(debug=True)
