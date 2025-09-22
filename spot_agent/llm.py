from langchain_ollama import ChatOllama


def get_ollama_chat_model(model_name, api_base="http://127.0.0.1:11435", temperature=0.8):
    return ChatOllama(
        model=model_name,
        base_url=api_base,
        num_ctx=32000,
        temperature=temperature,
    )