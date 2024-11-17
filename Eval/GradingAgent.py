from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

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
        f"Please provide detail evaluation on the interviewee's performance based on the following materials, strengths and weaknesses need to be discussed separately.\n"
        f"Transcript: {transcript_text}\n"
        f"Overall Score: {overall_score}/10, Recommendation Score: {recommendation_score}/10, Structured Answers Score: {structured_answers_score}/10.\n"
        f"Evaluation:\n\n"
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
            min_new_tokens=300,   
            do_sample=True,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    generated_tokens = output[0][inputs["input_ids"].shape[-1]:]
    evaluation = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    return evaluation

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
