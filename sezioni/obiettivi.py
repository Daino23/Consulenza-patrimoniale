import streamlit as st

def sezione_obiettivi():
    st.header("🎯 Obiettivi economici")

    if st.button("➕ Aggiungi obiettivo"):
        st.session_state.obiettivi_count += 1

    obiettivi = []
    for i in range(st.session_state.obiettivi_count):
        with st.expander(f"Obiettivo #{i+1}"):
            descrizione = st.text_input(f"Descrizione #{i+1}", key=f"ob_desc_{i}")
            importo = st.number_input(f"Importo da raggiungere (€) #{i+1}", min_value=0.0, step=500.0, key=f"ob_importo_{i}")
            tempo = st.text_input(f"Tempo previsto (es. 12 mesi) #{i+1}", key=f"ob_tempo_{i}")
            obiettivi.append(f"{descrizione} | {importo:.2f} € entro {tempo}")

    st.session_state["Obiettivi economici"] = obiettivi
