import streamlit as st

def sezione_obiettivi():
    st.header("🎯 Obiettivi economici")

    # Inizializza la lista per gli obiettivi se non esiste
    if "lista_obiettivi" not in st.session_state:
        st.session_state.lista_obiettivi = []

    # Bottone per aggiungere un nuovo obiettivo
    if st.button("➕ Aggiungi obiettivo"):
        # Aggiungi un dizionario vuoto alla lista
        st.session_state.lista_obiettivi.append({
            "Descrizione": "",
            "Importo Target": 0.0,
            "Tempo Previsto": ""
        })

    # Visualizza e permetti di modificare gli obiettivi esistenti
    if not st.session_state.lista_obiettivi:
        st.info("Nessun obiettivo aggiunto. Clicca 'Aggiungi obiettivo' per iniziare.")
    else:
        for i, obiettivo in enumerate(st.session_state.lista_obiettivi):
            with st.expander(f"Obiettivo #{i+1}: {obiettivo.get('Descrizione') or 'Nuovo Obiettivo'}", expanded=True):
                obiettivo["Descrizione"] = st.text_input(f"Descrizione #{i+1}", value=obiettivo["Descrizione"], key=f"ob_desc_{i}")
                obiettivo["Importo Target"] = st.number_input(f"Importo da raggiungere (€) #{i+1}", min_value=0.0, step=500.0, value=obiettivo["Importo Target"], format="%.2f", key=f"ob_importo_{i}")
                obiettivo["Tempo Previsto"] = st.text_input(f"Tempo previsto (es. 12 mesi) #{i+1}", value=obiettivo["Tempo Previsto"], key=f"ob_tempo_{i}")

                # Bottone per eliminare l'obiettivo
                if st.button(f"🗑️ Elimina Obiettivo #{i+1}", key=f"delete_ob_{i}"):
                    st.session_state.lista_obiettivi.pop(i)
                    st.success(f"Obiettivo #{i+1} eliminato.")
                    st.rerun()
    # (La riga st.session_state["Obiettivi economici"] = obiettivi non è più necessaria)
