# -*- coding: utf-8 -*-
# @Time : 2025/5/27 20:59
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1GT5xzyEae?t=327.0&p=3
# @File : Qwen2-vLLM-Local.py
# @Software: PyCharm 
# @Comment :
import os
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# 模型 ID :我们下载的模型全中文件目录
model_dir = '/home/nanji/workspace/DeepSeek-R1-Distill-Qwen-1.5B'

# Tokenizer 初始化
tokenizer = AutoTokenizer.from_pretrained(
    model_dir,
    # local_files_only=True,
    legacy=False  # 非严格
)
# Prompt 提示词
messages = [
    {'role': 'system', 'content': '你是一个智能问答助手.'},
    {'role': 'user', 'content': '天空为什么是蓝色的?'}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
# 初始化大语言模型
llm = LLM(
    model=model_dir,
    tensor_parallel_size=1,  # cpu无需张量并行
    dtype="float16"
)
# 超参数 ： 最多 512个 Token
sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05,
                                 max_tokens=512)
# 模型推理输出
outputs = llm.generate(
    [text],
    sampling_params
)
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f'Prompt提示词：{prompt!r},大模型推理输出 ：{generated_text!r}')
