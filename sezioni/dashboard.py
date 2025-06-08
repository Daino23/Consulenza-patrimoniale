# Contenuto del file: sezioni/dashboard.py (AGGIORNATO)

import streamlit as st
from datetime import date, datetime, timedelta # Aggiunto timedelta

def sezione_dashboard():
    """
    Questa funzione definisce il layout e il contenuto della Dashboard principale.
    Mostra informazioni riassuntive, la data corrente, note rapide e l'ultimo cliente/progetto.
    Ora include anche l'agenda giornaliera con i task.
    """
    st.header("📊 Dashboard Principale ✨")
    st.markdown("### Riepilogo Generale e Strumenti Rapidi per la Tua Consulenza.")

    # --- Sezione Riepilogo Superiore: Data, Note Rapide, Ultimo Cliente/Progetto ---
    col1, col2, col3 = st.columns([1, 1, 1.5])

    with col1:
        st.subheader("🗓️ Data Attuale")
        st.write(f"**Oggi è:** {date.today().strftime('%A %d %B %Y')}")
        st.markdown("---")

    with col2:
        st.subheader("📝 Note Rapide")
        st.text_area("Scrivi un appunto veloce qui...", value=st.session_state.get("dashboard_quick_notes_value", ""), height=100,
                     help="Queste note non vengono salvate permanentemente. Sono per la sessione corrente.",
                     key="dashboard_quick_notes")
        # Per salvare il valore del text_area se l'utente torna alla dashboard
        st.session_state.dashboard_quick_notes_value = st.session_state.dashboard_quick_notes

        st.markdown("---")

    with col3:
        st.subheader("👤 Ultimo Cliente/Progetto")
        if st.session_state.get('ultimo_cliente_progetto') and st.session_state['ultimo_cliente_progetto']['nome']:
            ultimo = st.session_state['ultimo_cliente_progetto']
            st.info(f"**Nome:** {ultimo.get('nome', 'N/D')}")
            st.write(f"**Ultimo Aggiornamento:** {ultimo.get('data', 'N/D')}")
        else:
            st.warning("Nessun cliente/progetto recente registrato. Compila la sezione 'Anagrafica Cliente'!")
        st.markdown("---")

    st.divider()

    # --- NUOVA SEZIONE: Agenda Giornaliera ---
    st.subheader("🗓️ Agenda di Oggi")
    today = date.today().isoformat()
    tasks_today = [
        task for task in st.session_state.get('tasks', [])
        if task['data_scadenza'] == today and not task['completato']
    ]

    if tasks_today:
        for i, task in enumerate(tasks_today):
            st.checkbox(f"**{task['descrizione']}** (Priorità: {task['priorita']})", value=task['completato'], key=f"dash_task_complete_{task['id']}", 
                        on_change=lambda t=task: update_task_status(t)) # Callback per aggiornare lo stato
    else:
        st.info("Nessun compito previsto per oggi. Ben fatto, o è ora di aggiungerne qualcuno!")

    # Funzione helper per aggiornare lo stato del task
    def update_task_status(task_to_update):
        for task in st.session_state.tasks:
            if task['id'] == task_to_update['id']:
                task['completato'] = not task['completato'] # Inverte lo stato
                break
        st.rerun() # Ricarica per riflettere il cambio immediatamente

    st.divider()

    # --- Sezione Indicatori Chiave e Riepiloghi (Mantenuti) ---
    st.subheader("📊 Indicatori Globali")

    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5) # Aggiunta colonna per Progetti
    with metric_col1:
        st.metric(label="Membri Famiglia", value=st.session_state.get('familiari_count', 0))
    with metric_col2:
        st.metric(label="Voci Patrimonio", value=st.session_state.get('patrimonio_count', 0))
    with metric_col3:
        st.metric(label="Voci Debiti", value=st.session_state.get('debiti_count', 0))
    with metric_col4:
        st.metric(label="Obiettivi Impostati", value=st.session_state.get('obiettivi_count', 0))
    with metric_col5: # NUOVO: Contatore Progetti
        st.metric(label="Progetti Attivi", value=len([p for p in st.session_state.get('progetti', []) if p['stato'] not in ['Completato', 'Archiviato', 'Annullato']]))

    st.markdown("---")

    # Riepilogo delle voci inserite (testuale, mantenuto)
    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:
        st.subheader("Riepilogo Dati Cliente")
        if 'cliente_data' in st.session_state and st.session_state.cliente_data['dati_personali']:
            st.write(f"**Cliente:** {st.session_state.cliente_data['dati_personali'].get('nome_cognome', 'N/D')}")
            st.write(f"**Professione:** {st.session_state.cliente_data['profilo_finanziario'].get('professione', 'N/D')}")
            st.write(f"**Stato Civile:** {st.session_state.cliente_data['dati_personali'].get('stato_civile', 'N/D')}")
            # Puoi aggiungere altri dettagli qui
        else:
            st.info("Nessun dato cliente principale inserito.")

        st.subheader("Patrimonio Inserito")
        patrimonio_list = st.session_state.get("beni_patrimoniali", []) # Ora legge da beni_patrimoniali
        if patrimonio_list:
            for item in patrimonio_list[:3]: # Mostra solo i primi 3 per concisione
                st.write(f"- {item.get('tipo', 'N/D')}: {item.get('valore', 0.0):.2f} €")
            if len(patrimonio_list) > 3:
                st.markdown(f"*(...altri {len(patrimonio_list) - 3} voci)*")
        else:
            st.info("Nessuna voce di patrimonio inserita.")

    with summary_col2:
        st.subheader("Debiti Registrati")
        debiti_list = st.session_state.get("lista_debiti", []) # Ora legge da lista_debiti
        if debiti_list:
            for item in debiti_list[:3]: # Mostra solo i primi 3
                st.write(f"- {item.get('tipo', 'N/D')}: {item.get('importo_mensile', 0.0):.2f} €/mese")
            if len(debiti_list) > 3:
                st.markdown(f"*(...altri {len(debiti_list) - 3} voci)*")
        else:
            st.info("Nessun debito ricorrente inserito.")

        st.subheader("Obiettivi Definiti")
        obiettivi_list = st.session_state.get("lista_obiettivi", []) # Ora legge da lista_obiettivi
        if obiettivi_list:
            for item in obiettivi_list[:3]: # Mostra solo i primi 3
                st.write(f"- {item.get('descrizione', 'N/D')} ({item.get('priorita', 'N/D')})")
            if len(obiettivi_list) > 3:
                st.markdown(f"*(...altri {len(obiettivi_list) - 3} voci)*")
        else:
            st.info("Nessun obiettivo economico definito.")

    st.divider()

    # --- Sezione Azioni Rapide / Promemoria (Mantenuta, con bottoni funzionanti) ---
    st.subheader("🚀 Azioni Rapide & Promemoria")
    st.write("Naviga rapidamente o visualizza promemoria per le sezioni principali.")

    # Funzione per cambiare sezione tramite bottone
    def navigate_to(section_name):
        st.session_state.sezione_corrente_radio = section_name
        st.rerun() # Forza il ricaricamento per applicare la navigazione

    quick_nav_col1, quick_nav_col2, quick_nav_col3 = st.columns(3)
    with quick_nav_col1:
        st.markdown("##### Dati Cliente:")
        st.button("Anagrafica Cliente 👤", on_click=lambda: navigate_to('Anagrafica Cliente'))
        st.button("Patrimonio 💼", on_click=lambda: navigate_to('Patrimonio'))
    with quick_nav_col2:
        st.markdown("##### Dati Finanziari:")
        st.button("Debiti 💳", on_click=lambda: navigate_to('Debiti'))
        st.button("Obiettivi 🎯", on_click=lambda: navigate_to('Obiettivi'))
    with quick_nav_col3:
        st.markdown("##### Gestione & Utilità:")
        st.button("Documenti 📄", on_click=lambda: navigate_to('Documenti'))
        st.button("Gestione Progetti 📋", on_click=lambda: navigate_to('Gestione Progetti'))
        st.button("To-Do List ✅", on_click=lambda: navigate_to('To-Do List'))


    st.success("Dashboard caricata con successo! Inserisci i dati nelle sezioni per vederli apparire qui.")
