import ollama
from concurrent.futures import ThreadPoolExecutor

models = ["llama3", "mistral", "phi3"]

def ask_model(model, question):

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": question}],
        options={
            "num_predict": 150
        },
        keep_alive="30m"
    )

    return model, response["message"]["content"]


def get_all_answers(question):

    answers = {}

    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda m: ask_model(m, question), models)

    for model, answer in results:
        answers[model] = answer

    return answers