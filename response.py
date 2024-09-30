from llama_cpp import Llama
import json

def classify_email_needs_response(email_json):
    llm = Llama(
        model_path="./meta-llama-3_2-3B-instruct-Q4_K_M.gguf",
        verbose=True,
        n_ctx=3048
    )

    email_content = email_json['body']
    
    messages = [
        {
            #sample prompt
            "role": "system",
            "content": (
                "You are a smart email assistant. Determine if the following email requires a response. "
                "Respond with JSON: {'needs_response': true} if it needs a response, and {'needs_response': false} if it does not."
                "\nThe email will need a response if:\n "
                "- There are questions that need to be answered\n"
                "- There needs to be follow up on their message\n"
                "- They are interested and want to learn more\n"
            )
        },
        {
            "role": "user",
            "content": f"Does the following email require a response?\n\n{email_content}"
        }
    ]

    completion = llm.create_chat_completion(
        stream=False,
        messages=messages,
        temperature=0.7,
        max_tokens=50,
           response_format={
        "type": "json_object",
                "schema": {
            "type": "object",
            "properties": {"needs_response": {"type": "bool"}},
            "required": ["needs_response"],
        },
        },
    )

    response = completion['choices'][0]['message']['content']

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {'needs_response': False}  