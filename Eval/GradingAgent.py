from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
from openai import OpenAI
import yaml
import os

device = torch.device('mps' if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

model_name = 'meta-llama/Llama-3.2-1B'
tokenizer = AutoTokenizer.from_pretrained(model_name,load_in_8bit=True, device_map='auto')
model = AutoModelForCausalLM.from_pretrained(model_name,device_map='auto')
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id
model.config.eos_token_id = tokenizer.eos_token_id


def getEval(transcript_text, overall_score, recommendation_score, structured_answers_score):
    prompt_text = (
    f"Please analyze the following interview transcript and provide a detailed evaluation. "
    f"Focus on strengths, weaknesses, and areas for improvement of the interviewee. Do not repeat the transcript verbatim.\n\n"
    f"Overall Score: {overall_score}/7, Recommendation Score: {recommendation_score}/7, "
    f"Structured Answers Score: {structured_answers_score}/7.\n\n"
    f"Transcript:\n{transcript_text}\n\n"
    f"Evaluation:\n"
    )

    # 确保模型在设备上
    model.to(device)
    inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
    
    # 调整生成设置
    with torch.no_grad():
        output = model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=500,  
            do_sample=True,
            temperature=0.7,  
            top_p=0.9, 
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    generated_tokens = output[0][inputs["input_ids"].shape[-1]:]
    evaluation = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    return evaluation

def getGptEval(transcript_text, overall_score, recommendation_score, structured_answers_score): 
    prompt_text = (
    f"Please analyze the following interview transcript and provide a detailed evaluation in 100 words. "
    f"Focus on strengths, weaknesses, and areas for improvement of the interviewee. Do not repeat the transcript verbatim.\n\n"
    f"Overall Score: {overall_score}/7, Recommendation Score: {recommendation_score}/7, "
    f"Structured Answers Score: {structured_answers_score}/7.\n\n"
    f"Transcript:\n{transcript_text}\n\n"
    f"Evaluation:\n"
    )

    with open(os.path.dirname(os.path.abspath(__file__))+"/openai_config.yaml", "r") as file:
        config = yaml.safe_load(file)
    client = OpenAI(
        organization=config['train']['organizationID'],
        project=config['train']['projectID'],
        api_key=config['train']['open_api_key'],
    )
    response = client.chat.completions.create(
      messages=[{"role": "user", "content": prompt_text}],
      model=config['train']['model']
    )
    return json.loads(response.json())['choices'][0]['message']['content']



if __name__ == "__main__":
    with open('../Labels/combined_data.json', 'r') as file:
        data = json.load(file)

    for p in data:
        transcript_text = data[p]["Transcript"]
        overall_score = data[p]["Overall"]
        recommendation_score = data[p]["RecommendHiring"]
        structured_answers_score = data[p]["StructuredAnswers"]
        print(f"Candidate {p} Evaluation:\n", getEval(transcript_text, overall_score, recommendation_score, structured_answers_score))
        print("\n" + "="*50 + "\n")
        break
