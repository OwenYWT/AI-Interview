import torch
import json
import yaml
from torch.utils.data import DataLoader
from dataset import HierarchicalInterviewDataset
from model import HierarchicalInterviewScorer
from sklearn.metrics import mean_squared_error
from os import path
import sys
sys.path.append("../Eval")
from GradingOnly import get_sentence_embedding
import pandas as pd
import joblib


config_path = "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
test_data_path = config["train"]["test_data_path"]

def calculate_feedback(predicted_scores, actual_scores):
    feedback_list = []
    score_labels = ["Overall Score", "Recommendation Score", "Structured Answers Score"]
    
    # Loop over each sample in the batch
    for idx in range(predicted_scores.size(0)):
        feedback = {}
        feedback_text = []
        
        for i, label in enumerate(score_labels):
            pred = predicted_scores[idx, i].item()
            actual = actual_scores[idx, i].item()
            diff = actual - pred
            
            feedback[label] = pred  # Store the predicted score for each label
            
            # Generate specific feedback based on the difference
            if abs(diff) > 1.0:
                if diff > 0:
                    feedback_text.append(f"Needs improvement in {label.lower()} as it was scored lower than expected.")
                else:
                    feedback_text.append(f"Good performance in {label.lower()} compared to the expected score.")
            else:
                feedback_text.append(f"Acceptable performance in {label.lower()}.")
        
        feedback["Feedback"] = " | ".join(feedback_text) if feedback_text else "Good overall performance!"
        feedback_list.append(feedback)
    return feedback_list

def load_basemodel():
    model = HierarchicalInterviewScorer().to(device)
    model.load_state_dict(torch.load(config["train"]["checkpoint_path"]))
    return model

def get_basemodel_eval(model,test_data):
    test_dataset = HierarchicalInterviewDataset(test_data)
    test_loader = DataLoader(test_dataset, batch_size=config["train"]["batch_size"], shuffle=False)
    all_true_scores = []
    all_predicted_scores = []

    model.eval()
    with torch.no_grad():
        for dialogue_turns, labels in test_loader:
            dialogue_turns = {k: v.to(device) for k, v in dialogue_turns.items()}
            labels = labels.to(device)
            predictions = model(dialogue_turns)
            all_true_scores.extend(labels.cpu().numpy())
            all_predicted_scores.extend(predictions.cpu().numpy())
    mse = mean_squared_error(all_true_scores, all_predicted_scores)
    return mse

def get_randomtree_eval(model_path,X,y_true):
    model = joblib.load(model_path)
    y_pred = model.predict(X)
    mse = mean_squared_error(y_true, y_pred)
    return mse

if __name__ == "__main__":
    with open(test_data_path, "r") as f:
        test_data = json.load(f)
    if config["eval"]["grading_model"] == "base_model":
        model = load_basemodel()
        mse = get_basemodel_eval(model,test_data)
        print(mse)
    else:
        records = [{
            "Transcript": values["Transcript"],
            "Overall": float(values["Overall"]),
            "RecommendHiring": float(values["RecommendHiring"]),
            "StructuredAnswers": float(values["StructuredAnswers"])
        } for values in test_data.values()]
        df = pd.DataFrame(records)
        df['Embeddings'] = df['Transcript'].apply(get_sentence_embedding)
        X = list(df['Embeddings'])

        Overall_mse = get_randomtree_eval(config["eval"]["tree_overall_model"], X, df['Overall'])
        RecommendHiring_mse = get_randomtree_eval(config["eval"]["tree_recommend_hiring_model"], X, df['RecommendHiring'])
        StructuredAnswers_mse = get_randomtree_eval(config["eval"]["tree_structured_answers_model"], X, df['StructuredAnswers'])
        print((Overall_mse+RecommendHiring_mse+StructuredAnswers_mse)/3)
    
    
    