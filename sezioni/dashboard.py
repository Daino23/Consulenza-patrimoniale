# Contenuto del file: /mount/src/consulenza-patrimoniale/sezioni/dashboard.py

import streamlit as st
from datetime import date

def sezione_dashboard():
    """
    Questa funzione definisce il layout e il contenuto della Dashboard principale.
    Mostra informazioni riassuntive, la data corrente, note rapide e l'ultimo cliente/progetto.
    """
    st.header("📊 Dashboard Principale ✨")
    st.markdown("### Riepilogo e Strumenti Rapidi")

    # --- Sezione Superiore: Data, Note Rapide, Ultimo Cliente/Progetto ---
    col1, col2, col3 = st.columns([1, 1, 1.5]) # Proporzioni per le colonne

    with col1:
        st.subheader("Data Attuale")
        st.write(f"🗓️ **Oggi è:** {date.today().strftime('%A %d %B %Y')}")
        st.markdown("---") # Linea separatrice

    with col2:
        st.subheader("Note Rapide")
        # Utilizziamo una key univoca per il text_area
        st.text_area("Scrivi un appunto qui...", value="", height=100,
                     help="Queste note non vengono salvate permanentemente. Sono per la sessione corrente.",
                     key="dashboard_quick_notes")
        st.markdown("---")

    with col3:
        st.subheader("Ultimo Cliente/Progetto")
        # Assumiamo che 'ultimo_cliente_progetto' sia salvato in st.session_state
        # Potrebbe essere un dizionario come {'nome': 'Mario Rossi', 'data': '2023-01-15'}
        if st.session_state.get('ultimo_cliente_progetto'):
            ultimo = st.session_state['ultimo_cliente_progetto']
            st.info(f"**Nome:** {ultimo.get('nome', 'N/D')}")
            st.write(f"**Ultimo Aggiornamento:** {ultimo.get('data', 'N/D')}")
            # Puoi aggiungere più dettagli qui se il tuo oggetto ultimo_cliente_progetto li contiene
        else:
            st.warning("Nessun cliente/progetto recente registrato. Inseriscine uno nelle sezioni dedicate!")
        st.markdown("---")

    st.divider() # Separatore visivo

    # --- Sezione Indicatori Chiave (Esempi) ---
    st.subheader("📈 Indicatori Globali")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    # Utilizziamo st.session_state per recuperare i contatori dalle altre sezioni
    with metric_col1:
        st.metric(label="Membri Famiglia", value=st.session_state.get('familiari_count', 0))
    with metric_col2:
        st.metric(label="Voci Patrimonio", value=st.session_state.get('patrimonio_count', 0))
    with metric_col3:
        st.metric(label="Voci Debiti", value=st.session_state.get('debiti_count', 0))
    with metric_col4:
        st.metric(label="Obiettivi Impostati", value=st.session_state.get('obiettivi_count', 0))

    st.divider()

    # --- Sezione Sezioni Rapide / Azioni Future (Esempio) ---
    st.subheader("📌 Azioni Rapide & Promemoria")
    st.write("Naviga rapidamente o visualizza promemoria per le sezioni principali.")

    # Esempio di un layout più complesso per le sezioni rapide
    quick_nav_col1, quick_nav_col2, quick_nav_col3 = st.columns(3)
    with quick_nav_col1:
        st.markdown("- [ ] **Famiglia**")
        st.markdown("- [ ] **Patrimonio**")
    with quick_nav_col2:
        st.markdown("- [ ] **Debiti**")
        st.markdown("- [ ] **Obiettivi**")
    with quick_nav_col3:
        st.markdown("- [ ] **Documenti**")
        # st.button("Vai a Documenti", key="go_doc_dash") # Esempio di bottone

    st.success("Dashboard caricata con successo! Inizia a inserire i dati per vederla prendere vita.")
