'''
uvicorn main:app --reload --host 0.0.0.0

'''
from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()
# 模型路径
# model_path = "/root/autodl-tmp/Models/deepseek-r1-1.5b-merged"
model_path = '/home/nanji/workspace/llm_stu/llama-fac/Models/deepseek-r1-1.5b-merged'
# 加载 tokenizer （分词器）
tokenizer = AutoTokenizer.from_pretrained(model_path)
# 加载模型并移动到可⽤设备（GPU/CPU）
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(model_path).to(device)


@app.get("/generate")
async def generate_text(prompt: str):
    # 使⽤ tokenizer 编码输⼊的 prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 使⽤模型⽣成⽂本
    outputs = model.generate(inputs["input_ids"], max_length=150)

    # 解码⽣成的输出
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"generated_text": generated_text}
