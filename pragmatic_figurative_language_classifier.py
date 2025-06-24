import json
import openai
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)


# Pragmatic Language Prompt Template
def build_pragmatic_prompt(user_text):

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
def build_figurative_prompt(user_text):
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

Respond only with the JSON. Keep it easy to understand, especially for someone who takes language literally.
"""


# Pragmatic Language Analysis
def analyze_literal_vs_figurative(user_text):
    prompt = build_figurative_prompt(user_text)
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
        raise e



# Literal vs Figurative Language Analysis
def analyze_literal_vs_figurative(user_text):
    prompt = build_figurative_prompt(user_text)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    content = response.choices[0].message.content
    return json.loads(content)


if __name__ == "__main__":
    # Example usage
    result1 = analyze_pragmatic_language("Can you stop talking while I'm working?")
    result2 = analyze_literal_vs_figurative("Break a leg in your performance!")

    print("Pragmatic Result:\n", result1)
    print("Figurative Result:\n", result2)
