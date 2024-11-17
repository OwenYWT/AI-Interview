import json
import torch
from transformers import BertTokenizer
import torch.nn.functional as F
from model import HierarchicalInterviewScorer
from model_utils import tokenize_dialogue, predict_scores, format_scores

# def load_trained_model(checkpoint_path, device="cpu"):
#     model = HierarchicalInterviewScorer(hidden_size=768, num_dialogue_layers=2, dropout=0.3)
#     state_dict = torch.load(checkpoint_path, map_location=device)
#     model.load_state_dict(state_dict, strict=False)
#     model = model.to(device)
#     return model

# if __name__ == "__main__":
#     checkpoint_path = "checkpoint1.pth" 
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model = load_trained_model(checkpoint_path, device=device)

#     conversation = input("Enter the entire conversation dialogue:\n")

#     dialogue_turns = [turn.strip() for turn in conversation.split('.') if turn.strip()]
#     dialogue_turns = ' '.join(dialogue_turns)
#     dialogue_dict = {"dialogue": dialogue_turns}
#     tokenized_input = tokenize_dialogue(dialogue_dict["dialogue"], max_turns=20, max_length=512)

#     if not dialogue_dict["dialogue"]:
#         print("No dialogue entered. Your score is 0")
#     else:
#         predicted_scores = predict_scores(model, tokenized_input, device=device)
        
#         formatted_scores = format_scores(predicted_scores)
#         print("\nPredicted Scores:")
#         for label, score in formatted_scores.items():
#             print(f"{label}: {score:.2f}")

    # val_data_path = "data/val_data.json"
    # with open(val_data_path, "r") as f:
    #     val_data = json.load(f)

    # sample_key = list(val_data.keys())[10] 
    # sample = val_data[sample_key]
    # tokenized_input = tokenize_dialogue(sample["Transcript"], max_turns=20, max_length=512)



    # model = load_trained_model("checkpoint1.pth", device=device)
    # predicted_scores = predict_scores(model, tokenized_input, device=device)
    # formatted_scores = format_scores(predicted_scores)

    # print("Predicted Scores:")
    # for label, score in formatted_scores.items():
    #     print(f"{label}: {score:.2f}")

    
    # dialogue = [
    #     "Hello, how are you today?",
    #     "I'm doing great, thank you!",
    #     "What about you?",
    #     "I'm good too. How can I assist you?"
    # ]
    
    # predicted_scores = predict_scores(model, dialogue, device=device)
    
    # formatted_scores = format_scores(predicted_scores)
    # print("Predicted Scores:")
    # for label, score in formatted_scores.items():
    #     print(f"{label}: {score:.2f}")



def load_trained_model(checkpoint_path, device="cpu"):

    model = HierarchicalInterviewScorer(hidden_size=768, num_dialogue_layers=2, dropout=0.3)
    state_dict = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(state_dict, strict=False)
    model = model.to(device)
    return model

def process_dialogue(conversation, max_turns=20, max_length=512):

    dialogue_turns = [turn.strip() for turn in conversation.split('.') if turn.strip()]
    dialogue_turns = ' '.join(dialogue_turns)
    dialogue_dict = {"dialogue": dialogue_turns}
    if not dialogue_dict["dialogue"]:
        return None, "No dialogue entered. Your score is 0"

    tokenized_input = tokenize_dialogue(dialogue_dict["dialogue"], max_turns=max_turns, max_length=max_length)
    return tokenized_input, None

def get_predicted_scores(model, tokenized_input, device="cpu"):

    predicted_scores = predict_scores(model, tokenized_input, device=device)
    formatted_scores = format_scores(predicted_scores)
    return formatted_scores

def run_interview_scorer(conversation, checkpoint_path="checkpoint1.pth", device=None):

    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_trained_model(checkpoint_path, device=device)
    tokenized_input, error_message = process_dialogue(conversation)
    if error_message:
        return {"Error": error_message}
    scores = get_predicted_scores(model, tokenized_input, device=device)
    return scores