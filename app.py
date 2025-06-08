import streamlit as st
from datetime import date
# Importa le sezioni aggiornate
from sezioni.cliente_anagrafica import sezione_cliente_anagrafica # Ho rinominato questo in `cliente_anagrafica.py`
from sezioni.patrimonio import sezione_patrimonio
from sezioni.debiti import sezione_debiti
from sezioni.obiettivi import sezione_obiettivi
from sezioni.documenti import sezione_documenti
from sezioni.dashboard import sezione_dashboard
from sezioni.gestione_progetti import sezione_gestione_progetti # Se l'hai aggiunta
from sezioni.todo_list import sezione_todo_list # Se l'hai aggiunta
from sezioni.crm import sezione_crm # Se l'hai aggiunta

# Inizializzazione dello stato sessione
# Non inizializziamo più i contatori qui, le sezioni si occuperanno di inizializzare le loro liste
if "cliente_data" not in st.session_state: # Questa è la nuova chiave per l'anagrafica centralizzata
    st.session_state.cliente_data = {
        "dati_personali": {},
        "profilo_finanziario": {},
        "dati_familiari": {"coniuge": None, "figli": [], "altri_familiari": []}
    }
# Inizializzazioni per le nuove liste strutturate (se non già presenti in altre sezioni)
if "beni_patrimoniali" not in st.session_state:
    st.session_state.beni_patrimoniali = []
if "lista_debiti" not in st.session_state:
    st.session_state.lista_debiti = []
if "lista_obiettivi" not in st.session_state:
    st.session_state.lista_obiettivi = []
if "crm_clients" not in st.session_state: # per il CRM
    st.session_state.crm_clients = []
if "projects" not in st.session_state: # per Gestione Progetti
    st.session_state.projects = []
if "todo_items" not in st.session_state: # per To-Do List
    st.session_state.todo_items = []


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
            "Anagrafica Cliente", # Ho rinominato Famiglia in Anagrafica Cliente
            "Patrimonio",
            "Debiti",
            "Obiettivi",
            "Documenti",
            "Gestione Progetti", # Se l'hai aggiunta
            "To-Do List", # Se l'hai aggiunta
            "CRM" # Se l'hai aggiunta
        ])

    # Logica per la visualizzazione delle sezioni
    if sezione == "Dashboard":
        sezione_dashboard()
    elif sezione == "Anagrafica Cliente": # Ho rinominato Famiglia in Anagrafica Cliente
        sezione_cliente_anagrafica()
    elif sezione == "Patrimonio":
        sezione_patrimonio()
    elif sezione == "Debiti":
        sezione_debiti()
    elif sezione == "Obiettivi":
        sezione_obiettivi()
    elif sezione == "Documenti":
        sezione_documenti()
    elif sezione == "Gestione Progetti": # Se l'hai aggiunta
        sezione_gestione_progetti()
    elif sezione == "To-Do List": # Se l'hai aggiunta
        sezione_todo_list()
    elif sezione == "CRM": # Se l'hai aggiunta
        sezione_crm()

if __name__ == "__main__":
    main()
