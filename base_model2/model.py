import torch
from torch import nn
from transformers import BertModel, AlbertModel
import torch.nn.functional as F

# class HierarchicalInterviewScorer(nn.Module):
#     def __init__(self, hidden_size=768, num_dialogue_layers=2, dropout=0.3):
#         super(HierarchicalInterviewScorer, self).__init__()
        
#         self.turn_encoder = BertModel.from_pretrained("bert-base-uncased")
        
#         self.dialogue_transformer = nn.TransformerEncoder(
#             nn.TransformerEncoderLayer(d_model=hidden_size, nhead=8, dropout=dropout),
#             num_layers=num_dialogue_layers
#         )
        
#         self.classifier = nn.Sequential(
#             nn.Linear(hidden_size, 256),
#             nn.ReLU(),
#             nn.Dropout(dropout),
#             nn.Linear(256, 3)
#         )
        
#     def forward(self, dialogue_turns):
#         batch_size, num_turns = dialogue_turns["input_ids"].shape[:2]
#         input_ids = dialogue_turns["input_ids"].view(-1, dialogue_turns["input_ids"].size(-1))
#         attention_mask = dialogue_turns["attention_mask"].view(-1, dialogue_turns["attention_mask"].size(-1))
        
#         turn_embeddings = self.turn_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0, :]
#         turn_embeddings = turn_embeddings.view(batch_size, num_turns, -1)
        
#         dialogue_embeddings = self.dialogue_transformer(turn_embeddings.permute(1, 0, 2))
#         dialogue_representation = dialogue_embeddings.mean(dim=0)
        
#         scores = self.classifier(dialogue_representation)
        
#         return scores


class TurnAttention(nn.Module):
    def __init__(self, hidden_size):
        super(TurnAttention, self).__init__()
        self.attention = nn.Linear(hidden_size, 1)

    def forward(self, turn_embeddings):
        scores = F.softmax(self.attention(turn_embeddings), dim=1)
        attended_representation = torch.sum(scores * turn_embeddings, dim=1)
        return attended_representation



class HierarchicalInterviewScorer(nn.Module):
    def __init__(self, hidden_size=768, num_dialogue_layers=2, dropout=0.3):
        super(HierarchicalInterviewScorer, self).__init__()
        
        self.turn_encoder = BertModel.from_pretrained("bert-base-uncased")
        for param in self.turn_encoder.parameters():
            param.requires_grad = True
        
        self.dialogue_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=hidden_size, nhead=8, dropout=dropout),
            num_layers=num_dialogue_layers
        )
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(hidden_size)
        self.turn_attention = TurnAttention(hidden_size)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_size, 256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 3)
        )
    def forward(self, dialogue_turns):
        batch_size, num_turns = dialogue_turns["input_ids"].shape[:2]
        input_ids = dialogue_turns["input_ids"].view(-1, dialogue_turns["input_ids"].size(-1))
        attention_mask = dialogue_turns["attention_mask"].view(-1, dialogue_turns["attention_mask"].size(-1))

        turn_embeddings = self.turn_encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state[:, 0, :]
        turn_embeddings = self.dropout(turn_embeddings)
        turn_embeddings = self.layer_norm(turn_embeddings)
        turn_embeddings = turn_embeddings.view(batch_size, num_turns, -1)
        
        dialogue_embeddings = self.dialogue_transformer(turn_embeddings.permute(1, 0, 2))
        dialogue_representation = dialogue_embeddings.mean(dim=0)
        
        scores = self.classifier(dialogue_representation)
        return scores
    

class HongzhenAlbertForRegression(nn.Module):
    def __init__(self, model_name, num_outputs=3):
        super(HongzhenAlbertForRegression, self).__init__()
        self.albert = AlbertModel.from_pretrained(model_name) 
        self.dropout = nn.Dropout(0.1)  
        self.regressor = nn.Linear(self.albert.config.hidden_size, num_outputs) 

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.albert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs[1]  
        pooled_output = self.dropout(pooled_output)
        predictions = self.regressor(pooled_output) 
        
        loss = None
        if labels is not None:
            loss_fn = nn.MSELoss() 
            loss = loss_fn(predictions, labels)
        
        return (loss, predictions) if loss is not None else predictions