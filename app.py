import streamlit as st
from datetime import date

# Importa le sezioni aggiornate
from sezioni.cliente_anagrafica import sezione_cliente_anagrafica
from sezioni.patrimonio import sezione_patrimonio
from sezioni.debiti import sezione_debiti
from sezioni.obiettivi import sezione_obiettivi
from sezioni.documenti import sezione_documenti
from sezioni.dashboard import sezione_dashboard
from sezioni.gestione_progetti import sezione_gestione_progetti # Nuova importazione
from sezioni.todo_list import sezione_todo_list # Nuova importazione


# Inizializzazione dello stato sessione per i contatori della dashboard
if "familiari_count" not in st.session_state:
    st.session_state.familiari_count = 0
if "patrimonio_count" not in st.session_state:
    st.session_state.patrimonio_count = 0
if "debiti_count" not in st.session_state:
    st.session_state.debiti_count = 0
if "obiettivi_count" not in st.session_state:
    st.session_state.obiettivi_count = 0
if "ultimo_cliente_progetto" not in st.session_state:
    st.session_state.ultimo_cliente_progetto = {'nome': 'Nessun cliente inserito', 'data': date.today().strftime("%Y-%m-%d")}


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
            "Anagrafica Cliente", # <--- Modificato qui
            "Patrimonio",
            "Debiti",
            "Obiettivi",
            "Documenti",
            "Gestione Progetti", # <--- Aggiunta nuova sezione
            "To-Do List"          # <--- Aggiunta nuova sezione
        ])

    # Logica per la visualizzazione delle sezioni
    if sezione == "Dashboard":
        sezione_dashboard()
    elif sezione == "Anagrafica Cliente": # <--- Modificato qui
        sezione_cliente_anagrafica()    # <--- Modificato qui
    elif sezione == "Patrimonio":
        sezione_patrimonio()
    elif sezione == "Debiti":
        sezione_debiti()
    elif sezione == "Obiettivi":
        sezione_obiettivi()
    elif sezione == "Documenti":
        sezione_documenti()
    elif sezione == "Gestione Progetti": # <--- Aggiunta nuova sezione
        sezione_gestione_progetti()
    elif sezione == "To-Do List":          # <--- Aggiunta nuova sezione
        sezione_todo_list()


if __name__ == "__main__":
    main()
