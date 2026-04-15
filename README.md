# 🚀 Multi-Model AI System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Mistral](https://img.shields.io/badge/Mistral-Model-orange)
![Phi-3](https://img.shields.io/badge/Phi--3-Model-blue)

---

## 🧠 Overview

The **Multi-Model AI System** is a Streamlit-based application that allows users to interact with, compare, and evaluate multiple AI models in one place.

This project goes beyond a simple chatbot by introducing:

* 🤖 Multi-model interaction
* 🧠 AI-to-AI debate
* ⚖️ AI Judge evaluation
* 🔍 Retrieval-Augmented Generation (RAG)
* 🏆 Leaderboard tracking
* ⚡ Performance monitoring

It demonstrates how combining multiple AI models can produce **better and more reliable outputs**.

---

## ✨ Key Features

### 🤖 Multi-Model Chat

Interact with multiple AI models simultaneously and compare responses.

### 🧠 AI Debate System

Models debate each other to improve answer quality.

### ⚖️ AI Judge

Automatically evaluates and ranks responses.

### 🔍 RAG System

Uses external documents to improve factual accuracy.

### 🏆 Leaderboard

Tracks performance of models.

### ⚡ Speed Tracking

Measures response time.

---

## 📸 Screenshots

### 🖥️ Chat Interface

![Chat](screenshots/chat.png)

### 🧠 AI Debate

![Debate](screenshots/debate.png)

### 🏆 Leaderboard

![Leaderboard](screenshots/leaderboard.png)

---

## ⚙️ Installation & Setup (Complete Guide)

Follow these steps to run the project locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/multi-model-ai-system.git
cd multi-model-ai-system
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install and Setup Ollama (Required)

This project uses local AI models via Ollama.

1. Download and install Ollama from:
   https://ollama.com

2. Pull required models:

```bash
ollama pull mistral
ollama pull phi3
```

3. Test a model:

```bash
ollama run mistral
```

If the model responds correctly, setup is complete ✅

---

### 5️⃣ Run the Streamlit App

```bash
streamlit run app.py
```

---

### 6️⃣ Open in Browser

If it doesn’t open automatically:

```
http://localhost:8501
```

---

## 🔁 Changing Models

You can easily switch models.

### Step 1: Open `models.py`

### Step 2: Change model name

```python
model_name = "mistral"
```

### Step 3: Replace with another model

```python
model_name = "llama3"
```

### Step 4: Download new model

```bash
ollama pull llama3
```

### Step 5: Restart the app

```bash
streamlit run app.py
```

---

## 🤖 Default Models

This project is configured to use:

* **Ollama**
* **Mistral**
* **Phi-3**

These models are:

* Lightweight
* Fast
* Suitable for local usage

---

## 📂 Project Structure

```
multi-model-ai-system/
│── app.py
│── evaluator.py
│── models.py
│── rag_system.py
│── requirements.txt
│── README.md
│── leaderboard.json
│── speed.json
│
├── data/
│   ├── debate.json
│   ├── doc.json
│   ├── rank.json
│   ├── refine.json
│
├── screenshots/
```

---

## 📊 Data Files

* `debate.json` → Stores debate interactions
* `doc.json` → RAG documents
* `rank.json` → Rankings
* `refine.json` → Refined responses

---

## ⚠️ Important Notes

* Local models must be installed separately
* Do NOT upload `.env` files
* Large model files are not included
* Ensure Ollama is running before using the app

---

## 🛠️ Customization

* Add models in `models.py`
* Modify evaluation in `evaluator.py`
* Improve RAG via `doc.json`
* Adjust token limits for better output

---

## 🐛 Troubleshooting

### App not running

* Check Python version (3.10+)
* Reinstall dependencies

### Model not responding

* Ensure model is installed
* Restart Ollama

### Slow performance

* Use smaller models
* Reduce token usage

---

## 🔮 Future Improvements

* Web-based UI (no Streamlit)
* More model integrations
* Better evaluation metrics
* UI/UX improvements

---

## 📄 License

Open-source and free to use.

---

## 🙌 Acknowledgement

Built as a multi-model AI experimentation system exploring collaborative intelligence.