# Contenuto del file: sezioni/todo_list.py

import streamlit as st
from datetime import date, datetime

def sezione_todo_list():
    st.header("✅ La Tua To-Do List")
    st.markdown("Gestisci i tuoi compiti e attività quotidiane.")

    # Inizializza la lista dei task se non esiste
    if "tasks" not in st.session_state:
        st.session_state.tasks = [] # Ogni task sarà un dizionario

    # Form per aggiungere un nuovo task
    st.subheader("➕ Aggiungi Nuovo Task")
    with st.form("form_nuovo_task", clear_on_submit=True):
        descrizione_task = st.text_input("Descrizione del Task", key="input_desc_task")
        data_scadenza_str = st.date_input("Data Scadenza", value=date.today(), key="input_data_scad_task")
        priorita_options = ["Bassa", "Media", "Alta", "Urgentissimo"]
        priorita_task = st.selectbox("Priorità", priorita_options, key="input_priorita_task")

        submitted = st.form_submit_button("Salva Task")
        if submitted:
            if descrizione_task:
                new_task = {
                    "id": datetime.now().timestamp(), # ID univoco
                    "descrizione": descrizione_task,
                    "data_scadenza": data_scadenza_str.isoformat(),
                    "priorita": priorita_task,
                    "completato": False, # Flag per lo stato del task
                    "data_creazione": date.today().isoformat()
                }
                st.session_state.tasks.append(new_task)
                st.success(f"Task '{descrizione_task}' aggiunto!")
            else:
                st.error("La descrizione del task non può essere vuota.")

    st.divider()

    # Visualizzazione e gestione dei task esistenti
    st.subheader("🗒️ Tutti i Task")

    if not st.session_state.tasks:
        st.info("Nessun task ancora in lista. Aggiungine uno qui sopra!")
    else:
        # Filtri
        col_filters1, col_filters2, col_filters3 = st.columns(3)
        with col_filters1:
            filter_completato = st.selectbox("Stato Completamento:", ["Tutti", "Da Completare", "Completati"], key="filter_tasks_completato")
        with col_filters2:
            filter_priorita = st.selectbox("Filtra per Priorità:", ["Tutte"] + priorita_options, key="filter_tasks_priorita")
        with col_filters3:
            # Filtro per data (es. Oggi, Questa Settimana, Scaduti)
            filter_data = st.selectbox("Filtra per Data:", ["Tutti", "Oggi", "Questa Settimana", "Scaduti"], key="filter_tasks_data")


        tasks_filtrati = st.session_state.tasks

        # Applica filtri
        if filter_completato == "Da Completare":
            tasks_filtrati = [t for t in tasks_filtrati if not t['completato']]
        elif filter_completato == "Completati":
            tasks_filtrati = [t for t in tasks_filtrati if t['completato']]
        
        if filter_priorita != "Tutte":
            tasks_filtrati = [t for t in tasks_filtrati if t['priorita'] == filter_priorita]

        today = date.today()
        if filter_data == "Oggi":
            tasks_filtrati = [t for t in tasks_filtrati if t['data_scadenza'] == today.isoformat()]
        elif filter_data == "Questa Settimana":
            tasks_filtrati = [t for t in tasks_filtrati if datetime.fromisoformat(t['data_scadenza']).date() >= today and datetime.fromisoformat(t['data_scadenza']).date() <= today + timedelta(days=7)]
        elif filter_data == "Scaduti":
            tasks_filtrati = [t for t in tasks_filtrati if datetime.fromisoformat(t['data_scadenza']).date() < today and not t['completato']]


        # Ordinamento
        col_sort_task1, col_sort_task2 = st.columns(2)
        with col_sort_task1:
            sort_by_task = st.selectbox("Ordina per:", ["Data Scadenza", "Priorità", "Descrizione"], key="sort_tasks_by")
        with col_sort_task2:
            sort_order_task = st.radio("Ordine:", ["Crescente", "Decrescente"], key="sort_tasks_order", horizontal=True)

        if sort_by_task == "Data Scadenza":
            tasks_filtrati.sort(key=lambda x: datetime.fromisoformat(x['data_scadenza']), reverse=(sort_order_task == "Decrescente"))
        elif sort_by_task == "Priorità":
            priorita_map = {"Urgentissimo": 4, "Alta": 3, "Media": 2, "Bassa": 1}
            tasks_filtrati.sort(key=lambda x: priorita_map.get(x['priorita'], 0), reverse=(sort_order_task == "Decrescente"))
        elif sort_by_task == "Descrizione":
            tasks_filtrati.sort(key=lambda x: x['descrizione'].lower(), reverse=(sort_order_task == "Decrescente"))


        for i, task in enumerate(tasks_filtrati):
            # Usiamo un layout a colonne per il singolo task
            task_col1, task_col2, task_col3 = st.columns([0.1, 0.7, 0.2]) # Checkbox, Descrizione, Data/Priorità

            with task_col1:
                # Checkbox per marcare come completato
                task['completato'] = st.checkbox("", value=task['completato'], key=f"task_completato_{task['id']}")
            
            with task_col2:
                task_text = f"**{task['descrizione']}**"
                if task['completato']:
                    st.markdown(f"~~{task_text}~~") # Testo barrato se completato
                else:
                    st.markdown(task_text)
            
            with task_col3:
                st.markdown(f"*{task['priorita']}*")
                st.markdown(f"Scad.: {task['data_scadenza']}")
            
            with st.expander(f"Modifica/Dettagli Task '{task['descrizione']}'", expanded=False):
                # Permette la modifica dei campi
                task['descrizione'] = st.text_input("Descrizione Task", value=task['descrizione'], key=f"edit_desc_task_{task['id']}")
                task['data_scadenza'] = st.date_input("Data Scadenza", value=datetime.fromisoformat(task['data_scadenza']), key=f"edit_data_scad_task_{task['id']}").isoformat()
                
                priorita_index = priorita_options.index(task['priorita']) if task['priorita'] in priorita_options else 0
                task['priorita'] = st.selectbox("Priorità", priorita_options, index=priorita_index, key=f"edit_priorita_task_{task['id']}")
                
                if st.button("🗑️ Elimina Task", key=f"delete_task_{task['id']}"):
                    st.session_state.tasks.remove(task)
                    st.success("Task eliminato.")
                    st.rerun()
            st.markdown("---") # Separatore per ogni task

    st.markdown("---")
    st.info("I tuoi task vengono salvati automaticamente.")