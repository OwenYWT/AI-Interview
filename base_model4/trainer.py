import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import tqdm
from model import HierarchicalInterviewScorer
from dataset import HierarchicalInterviewDataset
from eval import calculate_feedback

class Trainer:
    def __init__(self, model, train_loader, val_loader, optimizer, device, max_epochs):
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.device = device
        self.max_epochs = max_epochs

    def train(self):
        for epoch in range(self.max_epochs):
            self.model.train()
            train_loss = 0.0
            for dialogue_turns, labels in tqdm(self.train_loader):
                dialogue_turns = {k: v.to(self.device) for k, v in dialogue_turns.items()}
                labels = labels.to(self.device)

                outputs = self.model(dialogue_turns)
                loss = torch.nn.functional.mse_loss(outputs, labels)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item()

            print(f"Epoch {epoch + 1} | Train Loss: {train_loss / len(self.train_loader)}")
            self.evaluate()

    def evaluate(self):
        self.model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for dialogue_turns, labels in self.val_loader:
                dialogue_turns = {k: v.to(self.device) for k, v in dialogue_turns.items()}
                labels = labels.to(self.device)

                outputs = self.model(dialogue_turns)
                val_loss += torch.nn.functional.mse_loss(outputs, labels).item()

                feedback = calculate_feedback(outputs, labels)

        print(f"Validation Loss: {val_loss / len(self.val_loader)}")
