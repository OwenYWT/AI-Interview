# AI-Interview
## Group 7

Create a conda environment with `conda env create -f environment.yml`

To run backend server, run `python backend.py`
Note that it might take some time to setup for the first run

To run our frontend, run
`cd frontend`
`npm install`
`npm start`

To see frontend, open Google Chrome and visit http://localhost:3000/chat
Note that you MUST use Google Chrome for compatibility issues. 

Our codebase is set up to use either ollama for base model and transformers pipeline for fine tuned models. 
We found it easier to allow ollama to download the appropriate model on its own rather than including our fine-tuend model of 6GB. 

Each base_model folder contains an implementation of BERT based grading model. Each of them contains a pythons file for inference
Note that in our web app, the final grading requires remotely connected to one of the grading model (since running two or more LLMs on device at the same time is difficult with limited hardware.) 