#!/usr/bin/env python
# coding: utf-8

# In[7]:


import json
from dataset import InterviewDataset,HierarchicalInterviewDataset
from model import HongzhenAlbertForRegression
from torch.utils.data import Dataset, DataLoader
import yaml
from transformers import AlbertTokenizer,Trainer,TrainingArguments
import torch


# In[9]:


config_path = "config.yaml"
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")

with open(config_path, "r") as file:
    config = yaml.safe_load(file)

with open(config["train"]["train_data_path"], "r") as f:
    train_data = json.load(f)
with open(config["train"]["val_data_path"], "r") as f:
    val_data = json.load(f)

tokenizer = AlbertTokenizer.from_pretrained("albert-base-v2")

train_dataset = InterviewDataset(train_data, tokenizer)
val_dataset = InterviewDataset(val_data, tokenizer)
train_loader = DataLoader(train_dataset, batch_size=config["train"]["batch_size"], shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=config["train"]["batch_size"], shuffle=False)


# In[ ]:


model = HongzhenAlbertForRegression("albert-base-v2", num_outputs=3)
# 将模型移动到设备
model.to(device)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=config["train"]["max_epochs"],
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()

trainer.save_model("./saved_model")  # 将模型保存到指定目录

