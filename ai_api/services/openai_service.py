from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPEN_AI_KEY")
)

def ask_openai(message, tools=None):

    response = client.responses.create(
        model="gpt-5.5",
        input=message,
        tools=tools
    )

    return response