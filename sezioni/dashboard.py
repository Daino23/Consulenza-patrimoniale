import streamlit as st
from datetime import date
from sezioni.dashboard import sezione_dashboard
from sezioni.famiglia import sezione_famiglia
from sezioni.patrimonio import sezione_patrimonio
from sezioni.debiti import sezione_debiti
from sezioni.obiettivi import sezione_obiettivi
from sezioni.documenti import sezione_documenti

# Inizializzazione dello stato sessione
if "familiari_count" not in st.session_state:
    st.session_state.familiari_count = 0
if "patrimonio_count" not in st.session_state:
    st.session_state.patrimonio_count = 0
if "debiti_count" not in st.session_state:
    st.session_state.debiti_count = 0
if "obiettivi_count" not in st.session_state:
    st.session_state.obiettivi_count = 0

# Funzione principale per eseguire tutte le sezioni
def main():
    st.set_page_config(page_title="Consulenza Patrimoniale - Studio Dainotti", layout="wide")
    st.title("Scheda Consulenza Patrimoniale - Studio Dainotti")

    st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Navigazione")
        sezione = st.radio("Vai alla sezione:", [
            "Dashboard",
            "Famiglia",
            "Patrimonio",
            "Debiti",
            "Obiettivi",
            "Documenti"
        ])

    if sezione == "Dashboard":
        sezione_dashboard()
    elif sezione == "Famiglia":
        sezione_famiglia()
    elif sezione == "Patrimonio":
        sezione_patrimonio()
    elif sezione == "Debiti":
        sezione_debiti()
    elif sezione == "Obiettivi":
        sezione_obiettivi()
    elif sezione == "Documenti":
        sezione_documenti()

# Avvio dell'app
if __name__ == "__main__":
    main()
