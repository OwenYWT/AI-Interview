import torch
import json
import yaml
from torch.utils.data import DataLoader
from dataset import HierarchicalInterviewDataset
from model import HierarchicalInterviewScorer
from sklearn.metrics import mean_squared_error
import logging
import joblib

config_path = "config.yaml"
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

test_data_path = config["train"]["test_data_path"]

def calculate_feedback(predicted_scores, actual_scores):
    feedback_list = []
    score_labels = ["Overall Score", "Recommendation Score", "Structured Answers Score"]

    for idx in range(predicted_scores.size(0)):
        feedback = {}
        feedback_text = []

        for i, label in enumerate(score_labels):
            pred = predicted_scores[idx, i].item()
            actual = actual_scores[idx, i].item()
            diff = actual - pred

            feedback[label] = pred

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

def get_basemodel_eval(model, test_data):
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
