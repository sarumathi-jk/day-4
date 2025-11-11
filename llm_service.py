import requests
from app.config import settings

def generate_answer(query: str, context_docs: list[str]) -> str:
    """
    Generate a legal answer using a Hugging Face model hosted in the cloud.
    Combines query + retrieved context to form a grounded prompt.
    """
    prompt = f"""
You are a helpful legal assistant. Use the following context to answer the question accurately and concisely.

Context:
{chr(10).join(context_docs)}

Question: {query}

Answer:
"""

    url = f"https://api-inference.huggingface.co/models/{settings.hf_model_id}"
    headers = {"Authorization": f"Bearer {settings.hf_api_key}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 512}}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    # Extract generated text safely
    if isinstance(result, list) and "generated_text" in result[0]:
        return result[0]["generated_text"].split("Answer:")[-1].strip()
    elif isinstance(result, dict) and "generated_text" in result:
        return result["generated_text"]
    else:
        return str(result)
