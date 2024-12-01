import torch
from torch.utils.data import Dataset
from transformers import DistilBertTokenizer

class HierarchicalInterviewDataset(Dataset):
    def __init__(self, data, max_turns=20, max_length=128):
        self.data = list(data.values())
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        self.max_turns = max_turns
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        transcript = item["Transcript"]
        dialogue_turns = self.split_dialogue(transcript)

        encoded_turns = [self.tokenizer(turn, padding='max_length', max_length=self.max_length, truncation=True, return_tensors="pt") for turn in dialogue_turns[:self.max_turns]]

        while len(encoded_turns) < self.max_turns:
            encoded_turns.append(self.tokenizer("", padding='max_length', max_length=self.max_length, return_tensors="pt"))

        input_ids = torch.stack([et["input_ids"].squeeze(0) for et in encoded_turns])
        attention_mask = torch.stack([et["attention_mask"].squeeze(0) for et in encoded_turns])

        labels = torch.tensor([item["Overall"], item["RecommendHiring"], item["StructuredAnswers"]], dtype=torch.float)

        return {"input_ids": input_ids, "attention_mask": attention_mask}, labels

    def split_dialogue(self, transcript):
        parts = transcript.split('|')
        return [p.split(':', 1)[1].strip() for p in parts if ':' in p]
