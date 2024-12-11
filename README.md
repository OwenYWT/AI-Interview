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

Note that you MUST use Google Chrome for compatibility. 

Our codebase is set up to use either ollama for base model and transformers pipeline for fine tuned models. 
To test out functionality, we found it easier to allow ollama to download the appropriate model on its own rather than including our fine-tuend model of 20GB in total. 


Each base_model folder contains an implementation of BERT based grading model. Each of them contains a pythons file for inference.

Llama fine tuning is included in llama_finetune folder. Please note that Meta Llama requires access authorization and thus you will need to obtain access to gated model to run fine tune.
The fine tuning note book contains cells that allows you to test run the model with the model loaded. If you are instrested in trying with out fine-tuned checkpoint, please download it from: https://gtvault-my.sharepoint.com/:f:/g/personal/bsong74_gatech_edu/Et7ZsxiLD1FBoxNASe538yoBC6DRclFcpji9CpcUD0MgHw?e=q9Y2xp You will need GT credential to access.
Note that in our web app, the final grading requires remotely connected to one of the grading model (since running two or more LLMs on device at the same time is difficult with limited hardware.) 