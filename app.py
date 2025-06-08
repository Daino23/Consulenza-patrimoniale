# Contenuto del file: app.py

import streamlit as st
from datetime import date

# Importa le sezioni esistenti (con il nuovo nome per l'anagrafica)
from sezioni.cliente_anagrafica import sezione_cliente_anagrafica # MODIFICATO QUI
from sezioni.patrimonio import sezione_patrimonio
from sezioni.debiti import sezione_debiti
from sezioni.obiettivi import sezione_obiettivi
from sezioni.documenti import sezione_documenti
from sezioni.dashboard import sezione_dashboard

# --- NUOVE IMPORTAZIONI PER CRM E TO-DO LIST (saranno create nei prossimi passi) ---
# Per ora, le importiamo, creeremo i file vuoti temporaneamente
# e li riempiremo in seguito. Questo rende app.py pronto.
try:
    from sezioni.gestione_progetti import sezione_gestione_progetti
except ImportError:
    # Placeholder per evitare errori se il file non esiste ancora
    def sezione_gestione_progetti():
        st.subheader("Gestione Progetti (In costruzione)")
        st.info("Questa sezione è in fase di sviluppo. Torna presto!")
try:
    from sezioni.todo_list import sezione_todo_list
except ImportError:
    # Placeholder per evitare errori se il file non esiste ancora
    def sezione_todo_list():
        st.subheader("To-Do List (In costruzione)")
        st.info("Questa sezione è in fase di sviluppo. Torna presto!")
# --- FINE NUOVE IMPORTAZIONI ---

# Inizializzazione dello stato sessione per tutti i dati e contatori
if "familiari_count" not in st.session_state:
    st.session_state.familiari_count = 0
if "patrimonio_count" not in st.session_state:
    st.session_state.patrimonio_count = 0
if "debiti_count" not in st.session_state:
    st.session_state.debiti_count = 0
if "obiettivi_count" not in st.session_state:
    st.session_state.obiettivi_count = 0

# NUOVE INIZIALIZZAZIONI: Per l'ultimo cliente/progetto e le nuove sezioni
if "ultimo_cliente_progetto" not in st.session_state:
    st.session_state.ultimo_cliente_progetto = None # Sarà un dizionario con nome e data

# Inizializzazione per la gestione progetti
if "progetti" not in st.session_state:
    st.session_state.progetti = [] # Lista di dizionari per i progetti

# Inizializzazione per la to-do list
if "tasks" not in st.session_state:
    st.session_state.tasks = [] # Lista di dizionari per i task

# Inizializzazione per la sezione corrente del radio (per navigazione tramite bottoni)
if 'sezione_corrente_radio' not in st.session_state:
    st.session_state.sezione_corrente_radio = "Dashboard"

# Funzione principale per eseguire tutte le sezioni
def main():
    st.set_page_config(page_title="Consulenza Patrimoniale - Studio Dainotti", layout="wide")
    st.title("Scheda Consulenza Patrimoniale - Studio Dainotti")

    # Stili CSS per un miglior padding (mantenuto)
    st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Navigazione")
        # Il valore di default è preso dallo stato della sessione per permettere il cambio tramite bottoni
        sezione = st.radio(
            "Vai alla sezione:",
            [
                "Dashboard",
                "Anagrafica Cliente", # MODIFICATO QUI
                "Patrimonio",
                "Debiti",
                "Obiettivi",
                "Documenti",
                "Gestione Progetti", # NUOVA SEZIONE
                "To-Do List"        # NUOVA SEZIONE
            ],
            index=[
                "Dashboard", "Anagrafica Cliente", "Patrimonio", "Debiti",
                "Obiettivi", "Documenti", "Gestione Progetti", "To-Do List"
            ].index(st.session_state.sezione_corrente_radio), # Per la navigazione con i bottoni
            key="main_navigation_radio"
        )
        # Aggiorna lo stato della sessione ogni volta che il radio cambia
        st.session_state.sezione_corrente_radio = sezione

    # Logica per la visualizzazione delle sezioni
    if sezione == "Dashboard":
        sezione_dashboard()
    elif sezione == "Anagrafica Cliente": # MODIFICATO QUI
        sezione_cliente_anagrafica()
    elif sezione == "Patrimonio":
        sezione_patrimonio()
    elif sezione == "Debiti":
        sezione_debiti()
    elif sezione == "Obiettivi":
        sezione_obiettivi()
    elif sezione == "Documenti":
        sezione_documenti()
    elif sezione == "Gestione Progetti": # NUOVA SEZIONE
        sezione_gestione_progetti()
    elif sezione == "To-Do List":       # NUOVA SEZIONE
        sezione_todo_list()

# Avvio dell'app
if __name__ == "__main__":
    main()
