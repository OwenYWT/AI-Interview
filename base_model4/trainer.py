import time
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import tqdm
from model import HierarchicalInterviewScorer
from dataset import HierarchicalInterviewDataset
from eval import calculate_feedback
import yaml

class Trainer:
    def __init__(self, model=None, train_loader=None, val_loader=None, optimizer=None, device=None, max_epochs=None, config_path=None):
        if config_path:
            with open(config_path, "r") as file:
                self.config = yaml.safe_load(file)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            train_data = HierarchicalInterviewDataset(self.config["train"]["train_data_path"])
            val_data = HierarchicalInterviewDataset(self.config["train"]["val_data_path"])
            self.train_loader = DataLoader(train_data, batch_size=self.config["train"]["batch_size"], shuffle=True)
            self.val_loader = DataLoader(val_data, batch_size=self.config["train"]["batch_size"], shuffle=False)
            self.model = HierarchicalInterviewScorer().to(self.device)
            self.optimizer = AdamW(self.model.parameters(), lr=self.config["train"]["learning_rate"])
            self.max_epochs = self.config["train"]["max_epochs"]
        else:
            self.model = model
            self.train_loader = train_loader
            self.val_loader = val_loader
            self.optimizer = optimizer
            self.device = device
            self.max_epochs = max_epochs

    def train(self):
        for epoch in range(self.max_epochs):

            start_time = time.time()

            self.model.train()
            train_loss = 0.0
            for dialogue_turns, labels in tqdm(self.train_loader, desc=f"Epoch {epoch + 1}/{self.max_epochs}"):
                dialogue_turns = {k: v.to(self.device) for k, v in dialogue_turns.items()}
                labels = labels.to(self.device)
                outputs = self.model(dialogue_turns)
                loss = torch.nn.functional.mse_loss(outputs, labels)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item()

            end_time = time.time()
            epoch_time = end_time - start_time

            print(f"Epoch {epoch + 1} completed in {epoch_time:.2f} seconds.")
            print(f"Train Loss: {train_loss / len(self.train_loader):.4f}")
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
                print(feedback)

        print(f"Validation Loss: {val_loss / len(self.val_loader):.4f}")
