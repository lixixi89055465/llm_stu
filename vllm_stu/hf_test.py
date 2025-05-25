# -*- coding: utf-8 -*-
# @Time : 2025/5/25 17:06
# @Author : nanji
# @Site : https://www.bilibili.com/video/BV1GdX6YGEnZ?t=824.1
# @File : hf_test.py
# @Software: PyCharm 
# @Comment :
from transformers import modeling_utils
if not hasattr(modeling_utils, "ALL_PARALLEL_STYLES") or modeling_utils.ALL_PARALLEL_STYLES is None:
    modeling_utils.ALL_PARALLEL_STYLES = ["tp", "none","colwise",'rowwise']


from transformers import AutoModelForCausalLM, AutoTokenizer
import os
import torch

os.environ["TORCHVISION_DISABLE_NMS"] = "1"

DEVICE = "cuda"
# model_dir = '/mnt/workspace/models/Qwen/0wen2.5-0.5B-Instruct'
model_dir = '/home/nanji/workspace/Qwen2.5-0.5B-Instruct'

model = AutoModelForCausalLM.from_pretrained(model_dir,
                                             torch_dtype=torch.float16,
                                             device_map="auto",
                                             low_cpu_mem_usage=True,
                                             config={"parallel_style": "none"}
                                             )

tokenizer = AutoTokenizer.from_pretrained(model_dir)

# 调用模型
# 定义提示词
prompt = "你好，请介绍下你自己。"
# 将提示词封装为Message

message = [{"role": "system", "content": "你是一个智能助手"},
           {"role": "user", "content": prompt}]
# 使用分词器的apply_chat template编码message, 添加提示词先不集成消息令牌化(转化为input_ids)
text = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True)  # 将待处理的文本令牌化并转化为模型的输入张量
model_inputs = tokenizer([text], return_tensors="pt").to(DEVICE)
# 将数据输入模型得到输出
response = model.generate(model_inputs.input_ids, max_new_tokens=512)
print(response)
# 对输出的内容解码
response = tokenizer.batch_decode(response, skip_special_tokens=True)
print(response)
