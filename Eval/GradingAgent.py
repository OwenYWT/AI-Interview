from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
# if device.type == 'mps': print("Using MPS backend.")
# else: print("MPS not available. Using CPU.")

model_name = 'meta-llama/Llama-3.2-1B'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id
model.config.eos_token_id = tokenizer.eos_token_id


def getEval(transcript_text, overall_score, recommendation_score, structured_answers_score):
    prompt_text = (
    f"Please provide detail evaluation on the interviewee's performance based on the following materials, strengths and weaknesses need to be discussed separately.\n"
    f"Transcript: {transcript_text}\n"
    f"Overall Score: {overall_score}, Recommendation Score: {recommendation_score}, Structured Answers Score: {structured_answers_score}.\n"
    f"Evaluation:\n\n"
)


    # 确保模型在设备上
    model.to(device)
    inputs = tokenizer(prompt_text, return_tensors="pt", padding=True).to(device)
    
    # 调整生成设置
    output = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=500,
        do_sample=True,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.eos_token_id,
    )
    
    generated_tokens = output[0][inputs["input_ids"].shape[-1]:]
    evaluation = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

    return evaluation


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
