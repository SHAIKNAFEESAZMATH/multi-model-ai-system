import ollama

def evaluate_answers(question, answers):

    prompt = f"""
You are evaluating AI answers.

Question:
{question}

Answers:
"""

    for model, answer in answers.items():
        prompt += f"\n{model}: {answer}\n"

    prompt += """

Which model gave the BEST answer?

Reply ONLY with the model name.

Example:
llama3
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    best_model = response["message"]["content"].strip().lower()

    return best_model