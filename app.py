import streamlit as st
import ollama
import subprocess
import json
import os
import time
import pandas as pd
import concurrent.futures
from streamlit_option_menu import option_menu

from evaluator import evaluate_answers
from models import get_all_answers
from rag_system import load_pdf, search_docs

# =========================
# START OLLAMA
# =========================
try:
    subprocess.Popen(["ollama", "serve"])
except:
    pass

st.set_page_config(page_title="AI Multi Model Lab", layout="wide")
st.title("🤖 Multi-Model AI Lab")

# =========================
# FILE SYSTEM
# =========================
DATA = "data"
os.makedirs(DATA, exist_ok=True)

FILES = {
    "Rank": f"{DATA}/rank.json",
    "Refine": f"{DATA}/refine.json",
    "Debate": f"{DATA}/debate.json",
    "Doc": f"{DATA}/doc.json"
}

LEADERBOARD = "leaderboard.json"
SPEED = "speed.json"

MODELS = ["llama3", "mistral", "phi3"]
MAX_TOKENS = 250   # 👈 CHANGE THIS ONLY (200–300 recommended)

for f in FILES.values():
    if not os.path.exists(f):
        json.dump({}, open(f, "w"))

if not os.path.exists(LEADERBOARD):
    json.dump({m: 0 for m in MODELS}, open(LEADERBOARD, "w"))

if not os.path.exists(SPEED):
    json.dump({m: [] for m in MODELS}, open(SPEED, "w"))

# =========================
# UTILS
# =========================
def load(file, default):
    try:
        return json.load(open(file))
    except:
        return default

def save(file, data):
    json.dump(data, open(file, "w"), indent=2)

def tokens(txt):
    return int(len(txt.split()) * 1.3)

# =========================
# AI JUDGE
# =========================
def ai_judge(question, answers):
    formatted = ""
    for m, a in answers.items():
        formatted += f"\nModel: {m}\nAnswer: {a}\n"

    prompt = f"""
Question:
{question}

{formatted}

Return best model name only.
"""

    res = ollama.chat(
    model="llama3",
    messages=[{"role": "user", "content": prompt}],
    options={
        "num_predict": 20,   # only need short answer
        "temperature": 0
    }
)

    return res["message"]["content"].strip().lower().split()[0]

# =========================
# SESSION STATE
# =========================
if "chat_ids" not in st.session_state:
    st.session_state.chat_ids = {}

if "counter" not in st.session_state:
    st.session_state.counter = 1

# =========================
# TOP MENU
# =========================
with st.popover("⋮"):
    if st.button("🔥 Reset Everything"):
        for f in FILES.values():
            json.dump({}, open(f, "w"))
        json.dump({m: 0 for m in MODELS}, open(LEADERBOARD, "w"))
        json.dump({m: [] for m in MODELS}, open(SPEED, "w"))
        st.success("Reset Done")
        st.rerun()

    if st.button("💀 Kill App"):
        os._exit(0)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    page = option_menu(
        "AI Modes",
        [
            "🏆 Rank Answers",
            "🧠 Refined Answer",
            "⚔️ AI Debate",
            "📄 Document Chat",
            "📊 Leaderboard",
            "📈 Benchmark",
            "⚡ Speed"
        ],
        icons=["trophy","cpu","activity","file-text","bar-chart","graph-up","speedometer"]
    )

MAP = {
    "🏆 Rank Answers": "Rank",
    "🧠 Refined Answer": "Refine",
    "⚔️ AI Debate": "Debate",
    "📄 Document Chat": "Doc"
}

mode = MAP.get(page)

# =========================
# CHAT SYSTEM
# =========================
if mode:

    chats = load(FILES[mode], {})

    if mode not in st.session_state.chat_ids:
        st.session_state.chat_ids[mode] = None

    if not chats:
        name = f"Chat {st.session_state.counter}"
        chats[name] = []
        save(FILES[mode], chats)
        st.session_state.chat_ids[mode] = name
        st.session_state.counter += 1
        st.rerun()

    if st.session_state.chat_ids[mode] not in chats:
        st.session_state.chat_ids[mode] = list(chats.keys())[0]

    if st.sidebar.button("➕ New Chat"):
        name = f"Chat {st.session_state.counter}"
        chats[name] = []
        save(FILES[mode], chats)
        st.session_state.chat_ids[mode] = name
        st.session_state.counter += 1
        st.rerun()

    st.sidebar.divider()

    for c in chats:
        col1, col2 = st.sidebar.columns([4,1])

        if col1.button(c, key=f"{mode}_{c}"):
            st.session_state.chat_ids[mode] = c
            st.rerun()

        if col2.button("🗑", key=f"{mode}_del_{c}"):
            del chats[c]
            save(FILES[mode], chats)
            st.session_state.chat_ids[mode] = None
            st.rerun()

    current = st.session_state.chat_ids[mode]
    if current:
        new = st.sidebar.text_input("Rename Chat", current)
        if new != current:
            chats[new] = chats.pop(current)
            save(FILES[mode], chats)
            st.session_state.chat_ids[mode] = new
            st.rerun()

    messages = chats.get(st.session_state.chat_ids[mode], [])

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# =========================
# MODEL RUN
# =========================
def run_model(model, prompt):
    start = time.time()
    res = ollama.chat(
    model=model,
    messages=[{"role":"user","content":prompt}],
    options={
        "num_predict": MAX_TOKENS,
        "temperature": 0.7
    }
)
    ans = res["message"]["content"]
    t = round(time.time()-start,2)
    return model, ans, t, tokens(ans)

# =========================
# RANK
# =========================
if page == "🏆 Rank Answers":

    auto = st.toggle("⚖️ AI Judge", False)
    prompt = st.chat_input("Ask something...")

    if prompt:
        chats = load(FILES["Rank"], {})
        key = st.session_state.chat_ids["Rank"]

        messages = chats.get(key, [])
        messages.append({"role":"user","content":prompt})

        answers = {}
        speed = load(SPEED, {m:[] for m in MODELS})
        full_output = ""

        with concurrent.futures.ThreadPoolExecutor() as ex:
            futures = [ex.submit(run_model,m,prompt) for m in MODELS]

            for f in concurrent.futures.as_completed(futures):
                m,a,t,tk = f.result()
                answers[m]=a
                speed[m].append({"time":t,"tokens":tk})

                with st.chat_message("assistant"):
                    st.markdown(f"### {m}")
                    st.write(a)
                    st.caption(f"⏱ {t}s | 🔢 {tk}")

                full_output += f"### {m}\n{a}\n⏱ {t}s | 🔢 {tk}\n\n"

        save(SPEED, speed)

        best = ai_judge(prompt,answers) if auto else evaluate_answers(prompt,answers)
        st.success(f"🏆 Best Model: {best}")

        # 🔥 UPDATE LEADERBOARD
        leaderboard = load(LEADERBOARD, {m:0 for m in MODELS})

        if best in leaderboard:
             leaderboard[best] += 1
        else:
          leaderboard[best] = 1

        save(LEADERBOARD, leaderboard)

        full_output += f"\n🏆 Best Model: {best}"

        messages.append({"role":"assistant","content":full_output})
        chats[key] = messages
        save(FILES["Rank"],chats)

# =========================
# REFINE
# =========================
elif page == "🧠 Refined Answer":

    prompt = st.chat_input("Ask...")

    if prompt:
        chats = load(FILES["Refine"], {})
        key = st.session_state.chat_ids["Refine"]

        messages = chats.get(key, [])
        messages.append({"role":"user","content":prompt})

        answers = get_all_answers(prompt)
        full_output = ""

        for m,a in answers.items():
            st.markdown(f"### {m}")
            st.write(a)
            full_output += f"### {m}\n{a}\n\n"

        final = ollama.chat(
            model="llama3",
            messages=[{"role":"user","content":f"Combine:\n{answers}"}]
        )["message"]["content"]

        st.subheader("Refined Answer")
        st.write(final)

        full_output += f"\n### Final Answer\n{final}"

        messages.append({"role":"assistant","content":full_output})
        chats[key] = messages
        save(FILES["Refine"],chats)

# =========================
# DEBATE
# =========================
elif page == "⚔️ AI Debate":

    prompt = st.chat_input("Debate...")

    if prompt:
        chats = load(FILES["Debate"], {})
        key = st.session_state.chat_ids["Debate"]

        messages = chats.get(key, [])
        messages.append({"role":"user","content":prompt})

        r1 = run_model("llama3",prompt)[1]
        r2 = run_model("mistral",r1)[1]
        r3 = run_model("phi3",r2)[1]

        st.write("### Llama3")
        st.write(r1)
        st.write("### Mistral")
        st.write(r2)
        st.write("### Final")
        st.write(r3)

        full_output = f"### Llama3\n{r1}\n\n### Mistral\n{r2}\n\n### Final\n{r3}"

        messages.append({"role":"assistant","content":full_output})
        chats[key] = messages
        save(FILES["Debate"],chats)

# =========================
# DOCUMENT CHAT
# =========================
elif page == "📄 Document Chat":

    uploaded = st.file_uploader("Upload PDF", type="pdf")

    if uploaded:
        with open("temp.pdf","wb") as f:
            f.write(uploaded.read())
        load_pdf("temp.pdf")
        st.success("Document ready")

    prompt = st.chat_input("Ask document...")

    if prompt:
        chats = load(FILES["Doc"], {})
        key = st.session_state.chat_ids["Doc"]

        messages = chats.get(key, [])
        messages.append({"role":"user","content":prompt})

        context = search_docs(prompt)
        answers = get_all_answers(prompt + context)

        full_output = ""

        for m,a in answers.items():
            st.markdown(f"### {m}")
            st.write(a)
            full_output += f"### {m}\n{a}\n\n"

        messages.append({"role":"assistant","content":full_output})
        chats[key] = messages
        save(FILES["Doc"],chats)

# =========================
# LEADERBOARD
# =========================
elif page == "📊 Leaderboard":
    data = load(LEADERBOARD,{})
    df = pd.DataFrame(data.items(),columns=["Model","Wins"])
    st.bar_chart(df.set_index("Model"))
    st.table(df)

# =========================
# BENCHMARK
# =========================
elif page == "📈 Benchmark":

    speed = load(SPEED, {m:[] for m in MODELS})

    rows = []
    for model, data in speed.items():
        for entry in data:
            rows.append({
                "model": model,
                "time": entry["time"],
                "tokens": entry["tokens"]
            })

    if not rows:
        st.warning("No benchmark data yet.")
    else:
        df = pd.DataFrame(rows)
        st.dataframe(df)
        st.bar_chart(df.groupby("model")["time"].mean())
        st.bar_chart(df.groupby("model")["tokens"].mean())

# =========================
# SPEED
# =========================
elif page == "⚡ Speed":
    speed = load(SPEED,{m:[] for m in MODELS})

    avg = {
        m: sum([x["time"] for x in v])/len(v) if v else 0
        for m,v in speed.items()
    }

    df = pd.DataFrame(avg.items(),columns=["Model","Avg Time"])
    st.bar_chart(df.set_index("Model"))
    st.table(df)