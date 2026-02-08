import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from toroidal.toroidal import (
    compute_derivatives,
    detect_toroidal_nodes,
    toroidal_score
)

st.set_page_config(
    page_title="Toroidal Orbit Analyzer",
    layout="wide"
)

st.title("🌀 Toroidal Orbit Analyzer")
st.markdown("Поиск зон компенсации (торовские узлы)")

uploaded = st.file_uploader(
    "Загрузите CSV с орбитальными данными",
    type=["csv"]
)

if uploaded:
    df = pd.read_csv(uploaded)

    st.subheader("Исходные данные")
    st.dataframe(df.head(200), use_container_width=True)

    cols = df.columns.tolist()

    time_col = st.selectbox(
        "Колонка времени",
        cols
    )

    coord_cols = st.multiselect(
        "Колонки координат (x, y, z или аналог)",
        [c for c in cols if c != time_col]
    )

    dt = st.number_input(
        "Δt (секунды)",
        value=60.0
    )

    if st.button("▶ Прогнать данные"):
        if not coord_cols:
            st.error("Выберите хотя бы одну координату")
        else:
            df_proc = compute_derivatives(df, coord_cols, dt)
            nodes = detect_toroidal_nodes(df_proc, coord_cols)

            df_proc["toroidal_node"] = nodes
            df_proc["toroidal_score"] = toroidal_score(df_proc, coord_cols)

            st.success(f"Найдено тороидальных узлов: {nodes.sum()}")

            st.subheader("Таблица тороидальных узлов")
            st.dataframe(
                df_proc[df_proc["toroidal_node"]],
                use_container_width=True
            )

            st.subheader("График (для скриншотов)")
            fig, ax = plt.subplots(figsize=(10, 4))

            main_col = coord_cols[0]
            ax.plot(df_proc[main_col], label=main_col)

            ax.scatter(
                df_proc.index[nodes],
                df_proc.loc[nodes, main_col],
                color="red",
                label="Toroidal nodes",
                zorder=3
            )

            ax.set_xlabel("Index / Time")
            ax.set_ylabel(main_col)
            ax.legend()

            st.pyplot(fig)

