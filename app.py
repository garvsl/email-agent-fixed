from llama_cpp import Llama

from convert import convert_json


def llm_complete(email_json):

    llm = Llama(
    model_path="./meta-llama-3_2-3B-instruct-Q4_K_M.gguf",
    verbose=True,
    n_ctx=3048
    )

    # put business details
    business_details = """
 

    """



    examples = [
        #put previous emails as example
    ]

    converted_examples = [convert_json(email) for email in examples]


    few_shot_examples = "\n\n---\n\n".join(converted_examples)



    #The email to respond to


    email = f"""
    {convert_json(email_json)}
    """

    print(email)

    messages = [
        {
            "role": "system",
            "content": (
                # put prompt here
                "\n\n"
                "Business details for your reference:\n"
                + business_details +
                "\nHere are examples of previous email responses for your reference:\n"
                + few_shot_examples 
            )
        },
        {
            "role": "user",
            "content": (
                "Please compose a reply to the following email:\n\n"
                + email +
                "\n\n"
                "In your response only include the email, and make sure to:\n"
                # instructions here
            )
        }
    ]

    import tiktoken
    tokenizer = tiktoken.get_encoding("gpt2")
    total_tokens = len(tokenizer.encode(str(messages)))
    print(f"Total tokens: {total_tokens}")

    completion = llm.create_chat_completion(
        stream=False,
        messages=messages,
        temperature=0.7, 
        max_tokens=300  
    )

    return completion