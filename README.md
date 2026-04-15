# 🚀 Multi-Model AI System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Mistral](https://img.shields.io/badge/Mistral-Model-orange)
![Phi-3](https://img.shields.io/badge/Phi--3-Model-blue)

---

## 🧠 Overview

The **Multi-Model AI System** is an advanced Streamlit-based application designed to compare, evaluate, and enhance responses from multiple AI models in a unified interface.

Unlike traditional chat applications, this system enables:

* Multi-model interaction
* AI-to-AI debate
* Automated evaluation (AI Judge)
* Response refinement
* Retrieval-Augmented Generation (RAG)

This project demonstrates how combining multiple AI systems can produce **more accurate, diverse, and intelligent outputs**.

---

## ✨ Key Features

### 🤖 Multi-Model Chat

Interact with multiple models simultaneously and compare outputs in real time.

### 🧠 AI Debate System

Models debate each other to improve answer quality.

### ⚖️ AI Judge

Automatically evaluates and ranks model responses.

### 🔍 RAG (Retrieval-Augmented Generation)

Enhances responses using external document knowledge.

### 🏆 Leaderboard

Tracks model performance using stored metrics.

### ⚡ Speed Tracking

Measures response latency across models.

---

## 📸 Screenshots

### 🖥️ Chat Interface

![Chat](screenshots/chat.png)

### 🧠 AI Debate

![Debate](screenshots/debate.png)

### 🏆 Leaderboard

![Leaderboard](screenshots/leaderboard.png)

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/multi-model-ai-system.git
cd multi-model-ai-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 🤖 Default Models

This project is optimized for:

* **Ollama**
* **Mistral**
* **Phi-3**

These models are lightweight and suitable for local execution.

---

## 📥 Model Setup (Using Ollama)

1. Install Ollama
2. Pull models:

```bash
ollama pull mistral
ollama pull phi3
```

3. Test a model:

```bash
ollama run mistral
```

---

## 🔧 Changing Models

You can easily switch models.

### Step 1: Open `models.py`

### Step 2: Change model name

```python
model_name = "mistral"
```

👉 Replace with:

```python
model_name = "llama3"
```

### Step 3: Download new model

```bash
ollama pull llama3
```

### Step 4: Restart app

```bash
streamlit run app.py
```

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

* `debate.json` → Stores debates
* `doc.json` → RAG documents
* `rank.json` → Rankings
* `refine.json` → Refined outputs

---

## ⚠️ Important Notes

* Local models must be installed separately
* `.env` files should NOT be uploaded
* Large model files are excluded
* Some features depend on model availability

---

## 🛠️ Customization

* Add new models in `models.py`
* Modify evaluation in `evaluator.py`
* Expand RAG using `doc.json`
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
* Improved evaluation metrics
* Better UI/UX

---

## 📄 License

Open-source and free to use.

---

## 🙌 Acknowledgement

Built as a multi-model AI experimentation system exploring collaborative intelligence.