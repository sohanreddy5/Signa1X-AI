
import streamlit as st
import yfinance as yf
import google.generativeai as genai

# ====== CONFIGURE GEMINI API ======
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

model = genai.GenerativeModel("models/gemini-flash-latest")

# ====== UI ======
st.set_page_config(page_title="SignalX AI", layout="wide")

st.title("📈 SignalX AI – Market Intelligence System")

stock_symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS)")

# ====== DATA AGENT ======
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="5d")
    return hist

# ====== NEWS AGENT ======
def get_news(symbol):
    return [
        f"{symbol} shows recent movement in the market",
        f"Analysts are discussing {symbol}'s performance",
        f"Investors are actively watching {symbol}"
    ]

# ====== SIGNAL AGENT ======
def generate_signals(data):
    signals = []

    if len(data) < 2:
        return ["Not enough data"]

    last_close = data["Close"].iloc[-1]
    prev_close = data["Close"].iloc[-2]

    if last_close > prev_close:
        signals.append("Uptrend detected")
    else:
        signals.append("Downtrend detected")

    change = ((last_close - prev_close) / prev_close) * 100

    if abs(change) > 2:
        signals.append("High volatility")

    return signals

# ====== AI DECISION AGENT ======
def analyze_with_ai(data, news, signals):
    prompt = f"""
    You are an expert stock analyst.

    Stock Data:
    {data.tail().to_string()}

    News:
    {news}

    Signals:
    {signals}

    Provide output in this format:

    📊 Summary:
    ⚠️ Risks:
    🚀 Opportunities:
    ✅ Final Recommendation (Buy/Hold/Sell with reason):

    Keep it simple for retail investors.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating AI response: {e}"

# ====== MAIN BUTTON ======
if st.button("Analyze"):
    if stock_symbol == "":
        st.warning("Please enter a stock symbol")
    else:
        data = get_stock_data(stock_symbol)
        news = get_news(stock_symbol)
        signals = generate_signals(data)

        st.subheader("📊 Data Agent Output")
        st.dataframe(data.tail())

        st.subheader("📰 News Agent Output")
        for n in news:
            st.write("- ", n)

        st.subheader("📈 Signal Agent Output")
        for s in signals:
            st.write("- ", s)

        result = analyze_with_ai(data, news, signals)

        st.subheader("🧠 Decision Agent Output")
        st.write(result)

# ====== SIDEBAR ======
st.sidebar.title("🚀 Opportunity Radar")

trending = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

for t in trending:
    st.sidebar.write(t)