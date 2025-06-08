# Contenuto del file: sezioni/gestione_progetti.py

import streamlit as st
from datetime import date, datetime

def sezione_gestione_progetti():
    st.header("📋 Gestione Progetti")
    st.markdown("Monitora lo stato di avanzamento delle tue consulenze e pratiche.")

    # Inizializza la lista dei progetti se non esiste
    if "progetti" not in st.session_state:
        st.session_state.progetti = []

    # Form per aggiungere un nuovo progetto
    st.subheader("➕ Aggiungi Nuovo Progetto")
    with st.form("form_nuovo_progetto", clear_on_submit=True):
        nome_progetto = st.text_input("Nome Progetto / Cliente Associato", key="input_nome_progetto")
        data_inizio_str = st.date_input("Data Inizio", value=date.today(), key="input_data_inizio")
        data_scadenza_str = st.date_input("Data Scadenza Prevista", value=date.today(), key="input_data_scadenza")
        stato_options = ["In Lavorazione", "In Attesa Cliente", "In Attesa Documenti", "Completato", "Archiviato", "Annullato"]
        stato_progetto = st.selectbox("Stato del Progetto", stato_options, key="input_stato_progetto")
        note_progetto = st.text_area("Note sul Progetto", key="input_note_progetto")

        submitted = st.form_submit_button("Salva Progetto")
        if submitted:
            if nome_progetto:
                new_project = {
                    "id": datetime.now().timestamp(), # ID univoco basato sul timestamp
                    "nome": nome_progetto,
                    "data_inizio": data_inizio_str.isoformat(), # Salva come stringa ISO per facilità
                    "data_scadenza": data_scadenza_str.isoformat(),
                    "stato": stato_progetto,
                    "note": note_progetto,
                    "data_creazione": date.today().isoformat()
                }
                st.session_state.progetti.append(new_project)
                st.success(f"Progetto '{nome_progetto}' aggiunto con successo!")
            else:
                st.error("Il nome del progetto non può essere vuoto.")

    st.divider()

    # Visualizzazione e gestione dei progetti esistenti
    st.subheader("📚 Tutti i Progetti")

    if not st.session_state.progetti:
        st.info("Nessun progetto ancora registrato. Aggiungi il tuo primo progetto qui sopra!")
    else:
        # Filtri e ordinamento
        filter_stato = st.selectbox("Filtra per Stato:", ["Tutti"] + list(set([p['stato'] for p in st.session_state.progetti])), key="filter_progetti_stato")
        
        col_sort1, col_sort2 = st.columns(2)
        with col_sort1:
            sort_by = st.selectbox("Ordina per:", ["Data Scadenza", "Nome", "Stato", "Data Inizio"], key="sort_progetti_by")
        with col_sort2:
            sort_order = st.radio("Ordine:", ["Crescente", "Decrescente"], key="sort_progetti_order", horizontal=True)

        progetti_filtrati = st.session_state.progetti
        if filter_stato != "Tutti":
            progetti_filtrati = [p for p in progetti_filtrati if p['stato'] == filter_stato]
        
        # Ordinamento
        if sort_by == "Data Scadenza":
            progetti_filtrati.sort(key=lambda x: datetime.fromisoformat(x['data_scadenza']), reverse=(sort_order == "Decrescente"))
        elif sort_by == "Nome":
            progetti_filtrati.sort(key=lambda x: x['nome'].lower(), reverse=(sort_order == "Decrescente"))
        elif sort_by == "Stato":
            progetti_filtrati.sort(key=lambda x: x['stato'], reverse=(sort_order == "Decrescente"))
        elif sort_by == "Data Inizio":
            progetti_filtrati.sort(key=lambda x: datetime.fromisoformat(x['data_inizio']), reverse=(sort_order == "Decrescente"))


        for i, progetto in enumerate(progetti_filtrati):
            with st.expander(f"**Progetto:** {progetto['nome']} | **Stato:** {progetto['stato']}", expanded=False):
                st.markdown(f"**Data Inizio:** {progetto['data_inizio']}")
                st.markdown(f"**Data Scadenza Prevista:** {progetto['data_scadenza']}")
                st.markdown(f"**Note:** {progetto['note']}")

                st.markdown("---")
                st.write("Modifica Progetto:")
                
                # Permette la modifica dei campi
                progetto['nome'] = st.text_input("Nome Progetto", value=progetto['nome'], key=f"edit_nome_progetto_{progetto['id']}")
                progetto['data_inizio'] = st.date_input("Data Inizio", value=datetime.fromisoformat(progetto['data_inizio']), key=f"edit_data_inizio_{progetto['id']}").isoformat()
                progetto['data_scadenza'] = st.date_input("Data Scadenza", value=datetime.fromisoformat(progetto['data_scadenza']), key=f"edit_data_scadenza_{progetto['id']}").isoformat()
                
                stato_progetto_index = stato_options.index(progetto['stato']) if progetto['stato'] in stato_options else 0
                progetto['stato'] = st.selectbox("Stato", stato_options, index=stato_progetto_index, key=f"edit_stato_progetto_{progetto['id']}")
                progetto['note'] = st.text_area("Note", value=progetto['note'], key=f"edit_note_progetto_{progetto['id']}")

                col_actions1, col_actions2 = st.columns(2)
                with col_actions1:
                    # In teoria i dati sono già aggiornati tramite le key. Questo bottone potrebbe servire per un feedback.
                    st.button("Salva Modifiche", key=f"update_progetto_{progetto['id']}", help="Le modifiche ai campi qui sopra sono già salvate automaticamente.")
                with col_actions2:
                    if st.button("🗑️ Elimina Progetto", key=f"delete_progetto_{progetto['id']}"):
                        st.session_state.progetti.remove(progetto)
                        st.success("Progetto eliminato.")
                        st.rerun() # Forza un refresh per rimuovere il progetto dalla lista