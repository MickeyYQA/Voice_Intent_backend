import json
import openai
import os

openai_api_key = os.environ.get("OPENAI_API_KEY") 
openai.api_base = "https://aicvw.com/v1"
client = openai.OpenAI(base_url="https://aicvw.com/v1",api_key=openai_api_key)


# Pragmatic Language Prompt Template
def build_pragmatic_prompt(user_text, language='en'):
    if language == 'zh':
        return f"""
你是一位沟通教练，帮助自闭症人士理解语言在社交场合中的使用方式。

这个人刚刚在对话中收到了这条消息：

"{user_text}"

请分析并以以下JSON格式返回你的输出：

{{
  "pragmatic_use": "[字面 / 间接 / 讽刺 / 情感表达 / 正式 / 非正式 / 社交得体 / 不得体]",
  "speaker_intent": "[说话者的意图，例如：表达情感、提问、开玩笑、给出反馈]",
  "interpretation": "[用友好的语言清楚解释说话者可能的意思]",
  "suggested_response": "[用户可以给出的礼貌、社交得体的回应示例]"
}}

只返回JSON块，不要额外解释。
"""
    else:
        return f"""
You are a communication coach helping an autistic individual understand how language is used in social situations.

The person just received this message in a conversation:

"{user_text}"

Please analyze and return your output in the following JSON format:

{{
  "pragmatic_use": "[literal / indirect / sarcastic / emotionally expressive / formal / informal / socially appropriate / inappropriate]",
  "speaker_intent": "[intent of the speaker, e.g., expressing emotion, asking a question, joking, giving feedback]",
  "interpretation": "[clear explanation of what the speaker likely meant in friendly language]",
  "suggested_response": "[an example of a polite, socially appropriate response the user could give]"
}}

Only return the JSON block with no extra explanation.
"""


# Literal vs Figurative Prompt Template
def build_figurative_prompt(user_text, language='en'):
    if language == 'zh':
        return f"""
你正在帮助一位自闭症人士理解对话中的某句话是字面意思、比喻意思还是讽刺意思。

这个人刚刚收到了这条消息：

"{user_text}"

请分析并以以下JSON格式返回你的输出：

{{
  "classification": "[字面 / 比喻 / 讽刺]",
  "meaning": "[解释这句话在这个语境中的真正含义]",
  "why": "[用简单清楚的话解释为什么它是比喻、讽刺或字面意思]",
  "suggested_understanding_or_reply": "[用户应该如何理解或回应这种语言的示例]"
}}

只返回JSON，不要额外解释。保持简单易懂，特别是对于按字面意思理解语言的人。
"""
    else:
        return f"""
You are helping an autistic individual understand whether something said in a conversation is literal, figurative, or sarcastic.

The person just received this message:

"{user_text}"

Please analyze and return your output in this JSON format:

{{
  "classification": "[literal / figurative / sarcastic]",
  "meaning": "[explain what the sentence really means in this context]",
  "why": "[explain why it is figurative, sarcastic, or literal — in simple, clear terms]",
  "suggested_understanding_or_reply": "[example of how the user should understand or respond to this type of language]"
}}

Respond only with the JSON with no extra explanation. Keep it easy to understand, especially for someone who takes language literally.
"""


# Pragmatic Language Analysis
def analyze_pragmatic_language(user_text, language='en'):

    prompt = build_pragmatic_prompt(user_text, language)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    content = response.choices[0].message.content

    try: 
        return json.loads(content)
    except Exception as e:
        print("Failed to parse response:", content)
        return {"error": "Failed to parse response", "details": str(e), "raw_content": content}
    


# Literal vs Figurative Language Analysis
def analyze_literal_vs_figurative(user_text, language='en'):
    prompt = build_figurative_prompt(user_text, language)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception as e:
        print("Failed to parse response:", content)
        return {"error": "Failed to parse response", "details": str(e), "raw_content": content}


if __name__ == "__main__":
    # Example usage
    # result1 = analyze_pragmatic_language("Can you stop talking while I'm working?")
    result2 = analyze_literal_vs_figurative("Wow! That was a good idea!!")

    # print("Pragmatic Result:\n", result1)
    print("Figurative Result:\n", result2)
