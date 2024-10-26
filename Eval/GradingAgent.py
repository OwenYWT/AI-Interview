from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

# Set up device
# device = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
device = torch.device('cpu')
# if device.type == 'mps':
#     print("Using MPS backend.")
# else:
#     print("MPS not available. Using CPU.")

model_name = 'meta-llama/Llama-3.2-1B'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.pad_token_id
model.config.eos_token_id = tokenizer.eos_token_id
torch.set_default_dtype(torch.float32)


def getEval(transcript_text, overall_score, recommendation_score, structured_answers_score):
    prompt_text = (
    f"Based on the following interview transcript and scores, provide feedback addressing the candidate directly as 'you'.\n"
    f"Transcript: {transcript_text}\n\n"
    f"Scores:\n"
    f"- Overall Score: {overall_score}\n"
    f"- Recommendation Score: {recommendation_score}\n"
    f"- Structured Answers Score: {structured_answers_score}\n\n"
    "Evaluation (address the candidate directly as 'you' throughout):"
)


    # 确保模型在设备上
    model.to(device)
    inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
    
    # 调整生成设置
    output = model.generate(
        inputs["input_ids"],
        max_new_tokens=500,
        do_sample=True,
        repetition_penalty=1.1,
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
