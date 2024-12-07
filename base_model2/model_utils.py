from transformers import BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_dialogue(dialogue, max_turns=20, max_length=512):
    
    tokenized_turns = []

    for turn in dialogue[:max_turns]:
        encoded_turn = tokenizer(turn, padding='max_length', max_length=max_length, truncation=True, return_tensors="pt")
        tokenized_turns.append(encoded_turn)

    while len(tokenized_turns) < max_turns:
        tokenized_turns.append(tokenizer("", padding='max_length', max_length=max_length, return_tensors="pt"))

    input_ids = torch.stack([turn["input_ids"].squeeze(0) for turn in tokenized_turns])
    attention_mask = torch.stack([turn["attention_mask"].squeeze(0) for turn in tokenized_turns])

    return {
        "input_ids": input_ids.unsqueeze(0),
        "attention_mask": attention_mask.unsqueeze(0) 
    }

def predict_scores(model, tokenized_input, device="cpu"):
    model.eval()
    tokenized_input = {k: v.to(device) for k, v in tokenized_input.items()}
    with torch.no_grad(): 
        predicted_scores = model(tokenized_input)

    return predicted_scores.squeeze(0).cpu().numpy().tolist()

def format_scores(scores):
    
    score_labels = ["Overall Score", "Recommendation Score", "Structured Answers Score"]
    return {label: score for label, score in zip(score_labels, scores)}

def get_turn_attention_weights(attentions, input_ids, tokenizer, max_turns):
    
    last_layer_attention = attentions[-1]
    cls_attention = last_layer_attention[:, :, 0, :] 

    cls_attention = cls_attention.mean(dim=1)
    tokens = [tokenizer.decode(input_id) for input_id in input_ids[0]]

    turn_weights = []
    current_turn = 0
    turn_score = 0
    for token, attention in zip(tokens, cls_attention[0]):
        if "[SEP]" in token:
            turn_weights.append(turn_score)
            turn_score = 0
            current_turn += 1
        else:
            turn_score += attention.item()
    
    normalized_turn_weights = [score / sum(turn_weights) for score in turn_weights]

    return normalized_turn_weights

