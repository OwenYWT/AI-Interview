import os
import json
import pandas as pd
import torch
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from transformers import AutoTokenizer, AutoModel

# 环境变量设置以抑制 parallelism 警告
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 参数范围设定
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

# 加载模型与设备选择
device = torch.device("mps" if torch.backends.mps.is_built() else "cpu")
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)

def get_sentence_embedding(text):
    """生成文本的嵌入向量"""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy().flatten()

def train_and_save_model(X, y, model_path):
    """
    训练模型、评估并保存
    - X: 特征向量
    - y: 目标值
    - model_path: 模型保存路径
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(random_state=42)
    
    grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, 
                               scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # 评估模型
    y_pred = grid_search.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error for model: {mse}")

    # 保存模型
    joblib.dump(grid_search, model_path)
    print(f"Model saved to {model_path}")

# 加载数据
file_path = '../Labels/combined_data.json'  # 替换为你的文件路径
with open(file_path, 'r') as f:
    data = json.load(f)

# 数据解析并创建 DataFrame
records = [{
    "Transcript": values["Transcript"],
    "Overall": float(values["Overall"]),
    "RecommendHiring": float(values["RecommendHiring"]),
    "StructuredAnswers": float(values["StructuredAnswers"])
} for values in data.values()]

df = pd.DataFrame(records)

# 生成文本嵌入
df['Embeddings'] = df['Transcript'].apply(get_sentence_embedding)
X = list(df['Embeddings'])

# 训练并保存模型
train_and_save_model(X, df['Overall'], '../Models/y_overall_model.joblib')
train_and_save_model(X, df['RecommendHiring'], '../Models/y_recommend_hiring_model.joblib')
train_and_save_model(X, df['StructuredAnswers'], '../Models/y_structured_answers_model.joblib')
