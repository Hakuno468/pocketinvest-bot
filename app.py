# 1) まず全インポートをまとめて書く
import streamlit as st
import math, time, random               # ← 追加インポート
from openai import OpenAI, RateLimitError

# 2) OpenAI クライアントを生成
client = OpenAI(api_key=st.secrets["API_KEY"])

# 3) Streamlit タイトル
st.title("PocketInvest Bot")

# 4) ユーザー入力ウィジェット
amt = st.number_input("今日の支出額 (円)", step=1.0)

# 5) RateLimit 対応の safe_chat 関数
def safe_chat(prompt, retries=3):
    for _ in range(retries):
        try:
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        except RateLimitError:
            time.sleep(1 + random.random())
    return "⚠️ 混雑中です。しばらくして再度お試しください。"

# 6) 説明文を作るラッパー
def explain(invest, future):
    prompt = (
        f"Explain in two simple English sentences how investing ¥{invest} "
        f"of spare change every day grows to about ¥{int(future):,} in one year "
        f"at 5% annual interest. Make it upbeat."
    )
    return safe_chat(prompt)

# 7) メイン処理
if amt:
    invest = math.ceil(amt / 100) * 100 - amt
    future = invest * 365 * 1.05
    st.write(f"おつり投資額: **¥{int(invest)}** / 日")
    st.markdown(explain(invest, future))
