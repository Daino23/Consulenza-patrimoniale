import streamlit as st
from datetime import datetime

def sezione_crm():
    st.header("🤝 Gestione Relazioni Clienti (CRM)")
    st.markdown("Gestisci i contatti, le interazioni e lo storico dei tuoi clienti.")

    # Inizializza lo stato per i clienti CRM e le interazioni
    if "crm_clients" not in st.session_state:
        st.session_state.crm_clients = []

    # --- Gestione Aggiunta Nuovo Cliente CRM ---
    st.subheader("Aggiungi un Nuovo Cliente CRM")
    with st.expander("Dettagli Nuovo Cliente", expanded=False):
        with st.form("new_crm_client_form", clear_on_submit=True):
            new_client_name = st.text_input("Nome Cliente/Azienda", key="new_crm_client_name")
            new_client_contact_person = st.text_input("Referente (Nome e Cognome)", key="new_crm_contact_person")
            new_client_email = st.text_input("Email", key="new_crm_email")
            new_client_phone = st.text_input("Telefono", key="new_crm_phone")
            new_client_notes = st.text_area("Note Iniziali", key="new_crm_notes")

            submitted = st.form_submit_button("Aggiungi Cliente")
            if submitted and new_client_name:
                st.session_state.crm_clients.append({
                    "id": len(st.session_state.crm_clients) + 1,
                    "name": new_client_name,
                    "contact_person": new_client_contact_person,
                    "email": new_client_email,
                    "phone": new_client_phone,
                    "notes": new_client_notes,
                    "interactions": [] # Lista per le interazioni di questo cliente
                })
                st.success(f"Cliente '{new_client_name}' aggiunto al CRM.")
                st.rerun() # Forza il refresh per mostrare il nuovo cliente

    st.markdown("---")

    # --- Visualizzazione e Gestione Clienti Esistenti ---
    st.subheader("Elenco Clienti CRM")

    if not st.session_state.crm_clients:
        st.info("Nessun cliente nel CRM. Aggiungine uno per iniziare.")
    else:
        # Selettore per scegliere il cliente da visualizzare/modificare
        client_names = [client['name'] for client in st.session_state.crm_clients]
        selected_client_name = st.selectbox("Seleziona un Cliente:", ["Seleziona..."] + client_names, key="crm_client_selector")

        if selected_client_name != "Seleziona...":
            selected_client_index = client_names.index(selected_client_name)
            client = st.session_state.crm_clients[selected_client_index]

            st.write(f"### Dettagli Cliente: {client['name']}")
            st.markdown(f"**Referente:** {client.get('contact_person', 'N/A')}")
            st.markdown(f"**Email:** {client.get('email', 'N/A')}")
            st.markdown(f"**Telefono:** {client.get('phone', 'N/A')}")
            st.markdown(f"**Note:** {client.get('notes', 'N/A')}")

            st.markdown("---")
            st.write("#### Interazioni con il Cliente")

            # Form per aggiungere nuove interazioni
            with st.form(f"new_interaction_form_{client['id']}", clear_on_submit=True):
                interaction_type = st.selectbox("Tipo di Interazione", ["Chiamata", "Email", "Meeting", "Nota"], key=f"int_type_{client['id']}")
                interaction_date = st.date_input("Data Interazione", value=datetime.now().date(), key=f"int_date_{client['id']}")
                interaction_summary = st.text_area("Riepilogo Interazione", key=f"int_summary_{client['id']}")
                interaction_next_steps = st.text_area("Prossimi Passi / Azioni", key=f"int_next_steps_{client['id']}")

                interaction_submitted = st.form_submit_button("Aggiungi Interazione")
                if interaction_submitted and interaction_summary:
                    client["interactions"].append({
                        "timestamp": datetime.now().isoformat(), # Per ordinamento e unicità
                        "type": interaction_type,
                        "date": interaction_date.isoformat(),
                        "summary": interaction_summary,
                        "next_steps": interaction_next_steps
                    })
                    st.success("Interazione aggiunta.")
                    st.rerun()

            # Visualizzazione delle interazioni esistenti
            if not client["interactions"]:
                st.info("Nessuna interazione registrata per questo cliente.")
            else:
                st.markdown("##### Storico Interazioni:")
                # Ordina le interazioni dalla più recente alla meno recente
                sorted_interactions = sorted(client["interactions"], key=lambda x: x.get("timestamp", ""), reverse=True)

                for i, interaction in enumerate(sorted_interactions):
                    timestamp_dt = datetime.fromisoformat(interaction["timestamp"])
                    st.subheader(f"Interazione del {timestamp_dt.strftime('%d/%m/%Y %H:%M')}")
                    st.write(f"**Tipo:** {interaction['type']} (del {interaction['date']})")
                    st.info(f"**Riepilogo:** {interaction['summary']}")
                    if interaction.get('next_steps'):
                        st.warning(f"**Prossimi Passi:** {interaction['next_steps']}")

                    # Bottone per eliminare interazione
                    if st.button(f"🗑️ Elimina Interazione del {timestamp_dt.strftime('%d/%m/%Y %H:%M')}", key=f"delete_int_{client['id']}_{i}"):
                        client["interactions"].pop(client["interactions"].index(interaction))
                        st.success("Interazione eliminata.")
                        st.rerun()

            st.markdown("---")
            # Opzione per eliminare il cliente
            if st.button(f"⚠️ Elimina Cliente '{client['name']}'", key=f"delete_client_{client['id']}"):
                st.session_state.crm_clients.pop(selected_client_index)
                st.success(f"Cliente '{client['name']}' eliminato dal CRM.")
                st.rerun() # Forza il refresh dopo l'eliminazione
