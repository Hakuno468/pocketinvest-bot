import streamlit as st, openai, math

st.title("PocketInvest Bot")

# --- 入力 ---
amt = st.number_input("今日の支出額 (円)", step=1.0)

# --- APIキーを secrets から取得 ---
openai.api_key = st.secrets["API_KEY"]

def explain(invest, future):
    prompt = (
        f"Explain in two simple English sentences how investing ¥{invest} "
        f'of spare change every day grows to about ¥{int(future):,} in one year '
        f'at 5% annual interest. Make it upbeat.'
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

# --- 計算＆表示 ---
if amt:
    invest = math.ceil(amt/100)*100 - amt
    future = invest * 365 * 1.05
    st.write(f"おつり投資額: **¥{int(invest)}** / 日")
    st.write(explain(invest, future))
