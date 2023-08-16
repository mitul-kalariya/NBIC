import os
import sys
import openai
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse


# Fetch OpenAI API key from environment variable
OPENAI_API_KEY = "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"
if not len(OPENAI_API_KEY):
    print("Please set OPENAI_API_KEY environment variable.")
    sys.exit(1)
# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY
# Initialize FastAPI app
app = FastAPI(title="Simple API",)

def get_response_openai(prompt):
    try:
        prompt = prompt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            n=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            messages=[
                {"role": "system",
                 "content": "You possess expertise in aiding my comprehension of OOP and DS concepts.\
                             Kindly assist me in clarifying my foundational understanding."},
                {"role": "user", "content": prompt},
            ],
            stream=True
        )
        for chunk in response:
            current_content = chunk["choices"][0]["delta"].get("content", "")
            yield current_content
    except Exception as e:
        print("OpenAI Response (Streaming) error", str(e))
        return 503

@app.get(
    "/v1/chat/completions",
    tags=["APIs"],
    response_model=str,
)
def chat_completions(prompt: str = Query(...)):
    return StreamingResponse(get_response_openai("write a short note on lion"))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)


# ---------------
# Sample Test Client
# import requests
# url = "http://127.0.0.1:8000/v1/chat/completions/?prompt=Queue&quot;"
# response = requests.get(
#     url,
#     stream=True,
#     headers={"accept": "application/json"},
# )
# for chunk in response.iter_content(chunk_size=1024):
#     if chunk:
#         print(str(chunk, encoding="utf-8"), end="")