import streamlit as st

def sezione_patrimonio():
    st.header("💼 Area patrimoniale")

    # Inizializza la lista per i beni patrimoniali se non esiste
    if "beni_patrimoniali" not in st.session_state:
        st.session_state.beni_patrimoniali = []

    # Bottone per aggiungere un nuovo bene
    if st.button("➕ Aggiungi bene patrimoniale"):
        # Aggiungi un dizionario vuoto alla lista, che verrà popolato dall'expander
        st.session_state.beni_patrimoniali.append({
            "Tipo": "",
            "Descrizione": "",
            "Intestatario": "",
            "Valore": 0.0
        })

    # Visualizza e permetti di modificare i beni esistenti
    if not st.session_state.beni_patrimoniali:
        st.info("Nessun bene patrimoniale aggiunto. Clicca 'Aggiungi bene patrimoniale' per iniziare.")
    else:
        for i, bene in enumerate(st.session_state.beni_patrimoniali):
            # Usiamo un expander per ogni bene
            with st.expander(f"Bene #{i+1}: {bene.get('Descrizione') or 'Nuovo Bene'}", expanded=True):
                # Usiamo chiavi uniche per gli input Streamlit
                bene["Tipo"] = st.selectbox(f"Tipo di bene #{i+1}", ["Immobile", "Conto corrente", "Fondo", "ETF", "Trust", "Altro"], key=f"pat_tipo_{i}", index=["Immobile", "Conto corrente", "Fondo", "ETF", "Trust", "Altro"].index(bene["Tipo"]) if bene["Tipo"] else 0)
                bene["Descrizione"] = st.text_input(f"Descrizione #{i+1}", value=bene["Descrizione"], key=f"pat_desc_{i}")
                bene["Intestatario"] = st.text_input(f"Intestatario #{i+1}", value=bene["Intestatario"], key=f"pat_intest_{i}")
                bene["Valore"] = st.number_input(f"Valore stimato € #{i+1}", min_value=0.0, step=100.0, value=bene["Valore"], format="%.2f", key=f"pat_valore_{i}")

                # Bottone per eliminare il bene
                if st.button(f"🗑️ Elimina Bene #{i+1}", key=f"delete_pat_{i}"):
                    st.session_state.beni_patrimoniali.pop(i)
                    st.success(f"Bene #{i+1} eliminato.")
                    st.rerun() # Ricarica per aggiornare la lista

    # (La riga st.session_state["Situazione patrimoniale"] = patrimonio non è più necessaria)
