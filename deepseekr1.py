import os
from volcenginesdkarkruntime import Ark
# 从环境变量中读取您的方舟API Key
client = Ark(api_key="5234644f-dd06-47c9-9389-636c4cbd691b")


def chat(role:str="user", content:str="你好"):
    completion = client.chat.completions.create(
        # 替换 <Model>为 Model ID
        model="deepseek-r1-250120",
        messages=[
            {"role": role, "content": content}
        ]
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    print(chat(content="告诉我喝蛋白粉有用吗，人体不是能自动合成蛋白质吗，蛋白粉有多少必须氨基酸"))