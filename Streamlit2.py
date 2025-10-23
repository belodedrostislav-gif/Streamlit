# === OSINT-додаток "Компанія під мікроскопом" ===
# Спрощена версія для GitHub / Streamlit / Colab

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Функції ---

def get_company_data(name: str):
    """Імітація запиту до відкритих API (YouControl, SMIDA)."""
    # У реальному варіанті тут робиться requests.get(...)
    np.random.seed(len(name))
    years = [2020, 2021, 2022, 2023, 2024]
    data = {
        "year": years,
        "revenue": np.random.randint(5_000_000, 30_000_000, size=len(years)),
        "net_income": np.random.randint(-2_000_000, 5_000_000, size=len(years)),
        "assets": np.random.randint(10_000_000, 50_000_000, size=len(years)),
        "liabilities": np.random.randint(3_000_000, 25_000_000, size=len(years)),
    }
    df = pd.DataFrame(data)
    return df


def compute_risk(df: pd.DataFrame) -> dict:
    """Проста оцінка ризику."""
    latest = df.iloc[-1]
    risk = 0
    details = []

    if latest["net_income"] < 0:
        risk += 25
        details.append("Збиток у останньому році")
    if latest["liabilities"] / latest["assets"] > 0.6:
        risk += 25
        details.append("Висока заборгованість")
    if df["revenue"].iloc[-1] < df["revenue"].iloc[-2]:
        risk += 25
        details.append("Падіння виручки")
    if np.random.rand() < 0.2:
        risk += 25
        details.append("Негативні новини / санкції")

    return {"score": risk, "details": details}


# --- Інтерфейс Streamlit ---
st.set_page_config(page_title="Компанія під мікроскопом", layout="wide")
st.title("🔍 Компанія під мікроскопом")

company = st.text_input("Введіть назву компанії:", "Рошен")

if st.button("Пошук"):
    with st.spinner("Отримання даних..."):
        df = get_company_data(company)
        risk = compute_risk(df)

    st.subheader("📊 Фінансові показники")
    st.dataframe(df)

    # --- Графіки ---
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(df, x="year", y="revenue", title="Виручка за роками"))
    with col2:
        st.plotly_chart(px.line(df, x="year", y="net_income", title="Чистий прибуток"))

    # --- Оцінка ризику ---
    st.subheader("⚠️ Оцінка ризику")
    st.metric("Загальний ризик", f"{risk['score']} / 100")
    if risk["details"]:
        st.write("Причини підвищеного ризику:")
        for d in risk["details"]:
            st.write(f"• {d}")
    else:
        st.success("Ознак підвищеного ризику не виявлено ✅")

    # --- Збереження ---
    st.download_button(
        "💾 Завантажити CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name=f"{company}_data.csv",
        mime="text/csv",
    )
