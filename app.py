import streamlit as st, math
from openai import OpenAI            # ★ 旧: import openai → 新API

# ★ 旧: openai.api_key = st.secrets["API_KEY"]
client = OpenAI(                     # ★ 新クライアント
    api_key=st.secrets["API_KEY"]
)

st.title("PocketInvest Bot")

# ---- ユーザー入力 ----
amt = st.number_input("今日の支出額 (円)", step=1.0)

def explain(invest, future):
    prompt = (
        f"Explain in two simple English sentences how investing ¥{invest} "
        f"of spare change every day grows to about ¥{int(future):,} in one year "
        f"at 5% annual interest. Make it upbeat."
    )
    chat = client.chat.completions.create(   # ★ 旧: openai.ChatCompletion.create
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

# ---- 計算＆表示 ----
if amt:
    invest = math.ceil(amt / 100) * 100 - amt   # 切り上げ100円との差額
    future = invest * 365 * 1.05                # 年5%想定
    st.write(f"おつり投資額: **¥{int(invest)}** / 日")
    st.markdown(explain(invest, future))

