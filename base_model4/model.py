import torch
from torch import nn
from transformers import DistilBertModel

class HierarchicalInterviewScorer(nn.Module):
    def __init__(self, hidden_size=768, num_dialogue_layers=2, dropout=0.3):
        super(HierarchicalInterviewScorer, self).__init__()

        self.turn_encoder = DistilBertModel.from_pretrained("distilbert-base-uncased")

        self.dialogue_transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=hidden_size, nhead=8, dropout=dropout),
            num_layers=num_dialogue_layers
        )

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
        turn_embeddings = turn_embeddings.view(batch_size, num_turns, -1)

        dialogue_embeddings = self.dialogue_transformer(turn_embeddings.permute(1, 0, 2))
        dialogue_representation = dialogue_embeddings.mean(dim=0)

        scores = self.classifier(dialogue_representation)

        return scores
