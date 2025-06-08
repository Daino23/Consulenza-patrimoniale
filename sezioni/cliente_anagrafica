# Contenuto del file: sezioni/cliente_anagrafica.py

import streamlit as st
from datetime import date # Necessario per la data
from datetime import datetime # Necessario per datetime.fromisoformat

def sezione_cliente_anagrafica():
    st.header("👤 Anagrafica e Profilo Cliente")
    st.markdown("Raccogli qui le informazioni essenziali per la profilazione e segmentazione del cliente.")

    # Inizializza lo stato della sessione per questa sezione
    # Usiamo un dizionario più strutturato per i dati del cliente principale
    if "cliente_data" not in st.session_state:
        st.session_state.cliente_data = {
            "dati_personali": {},
            "dati_familiari": {"coniuge": {}, "figli": [], "altri_familiari": []},
            "profilo_finanziario": {}
        }
    
    # Inizializza has_children_checkbox per evitare errori al primo caricamento
    if "has_children_checkbox" not in st.session_state:
        st.session_state.has_children_checkbox = False # Default: no figli

    # Utilizziamo 'cliente_data' come riferimento più chiaro
    cliente_data = st.session_state.cliente_data

    # --- Sezione Dati Personali ---
    with st.expander("Dati Anagrafici del Cliente Principale", expanded=True):
        st.subheader("Informazioni Personali")
        col1, col2 = st.columns(2)
        with col1:
            # Assicurati che i valori siano pre-popolati per persistenza
            nome_cognome = st.text_input("Nome e Cognome", value=cliente_data["dati_personali"].get("nome_cognome", ""), key="cliente_nome_cognome")
            cliente_data["dati_personali"]["nome_cognome"] = nome_cognome
            
            # Per le date, è meglio usare st.date_input con un valore datetime.date
            # Gestiamo la conversione da stringa ISO (se già salvata) a oggetto date
            data_nascita_val = None
            if cliente_data["dati_personali"].get("data_nascita"):
                try:
                    data_nascita_val = datetime.fromisoformat(cliente_data["dati_personali"]["data_nascita"]).date()
                except ValueError:
                    data_nascita_val = date.today() # Fallback se il formato non è corretto
            else:
                data_nascita_val = date.today() # Default per nuovo inserimento
                
            cliente_data["dati_personali"]["data_nascita"] = st.date_input("Data di Nascita", value=data_nascita_val, key="cliente_data_nascita").isoformat()
            
            cliente_data["dati_personali"]["codice_fiscale"] = st.text_input("Codice Fiscale", value=cliente_data["dati_personali"].get("codice_fiscale", ""), key="cliente_codice_fiscale")
        with col2:
            cliente_data["dati_personali"]["luogo_nascita"] = st.text_input("Luogo di Nascita", value=cliente_data["dati_personali"].get("luogo_nascita", ""), key="cliente_luogo_nascita")
            cliente_data["dati_personali"]["indirizzo"] = st.text_input("Indirizzo di Residenza", value=cliente_data["dati_personali"].get("indirizzo", ""), key="cliente_indirizzo")
            cliente_data["dati_personali"]["telefono"] = st.text_input("Numero di Telefono", value=cliente_data["dati_personali"].get("telefono", ""), key="cliente_telefono")
            cliente_data["dati_personali"]["email"] = st.text_input("Indirizzo Email", value=cliente_data["dati_personali"].get("email", ""), key="cliente_email")

        # AGGIORNAMENTO PER DASHBOARD: l'ultimo cliente/progetto
        if nome_cognome:
            st.session_state.ultimo_cliente_progetto = {
                'nome': nome_cognome,
                'data': date.today().strftime("%Y-%m-%d") # Salva la data odierna come stringa
            }

    # --- Sezione Dati Familiari ---
    with st.expander("Composizione Familiare", expanded=False):
        st.subheader("Situazione Civile e Familiare")
        stato_civile_options = ["", "Celibe/Nubile", "Coniugato/a", "Separato/a", "Divorziato/a", "Vedovo/a", "Unito Civilmente"]
        stato_civile_index = stato_civile_options.index(cliente_data["dati_personali"].get("stato_civile", "")) if cliente_data["dati_personali"].get("stato_civile", "") in stato_civile_options else 0
        cliente_data["dati_personali"]["stato_civile"] = st.selectbox("Stato Civile", stato_civile_options, index=stato_civile_index, key="cliente_stato_civile")

        if cliente_data["dati_personali"]["stato_civile"] in ["Coniugato/a", "Unito Civilmente"]:
            st.markdown("##### Dati del Coniuge / Partner")
            cliente_data["dati_familiari"]["coniuge"]["nome_cognome"] = st.text_input("Nome e Cognome Coniuge/Partner", value=cliente_data["dati_familiari"]["coniuge"].get("nome_cognome", ""), key="coniuge_nome")
            
            coniuge_data_nascita_val = None
            if cliente_data["dati_familiari"]["coniuge"].get("data_nascita"):
                try:
                    coniuge_data_nascita_val = datetime.fromisoformat(cliente_data["dati_familiari"]["coniuge"]["data_nascita"]).date()
                except ValueError:
                    coniuge_data_nascita_val = date.today()
            else:
                coniuge_data_nascita_val = date.today()
            cliente_data["dati_familiari"]["coniuge"]["data_nascita"] = st.date_input("Data di Nascita Coniuge/Partner", value=coniuge_data_nascita_val, key="coniuge_data_nascita").isoformat()
            
            cliente_data["dati_familiari"]["coniuge"]["codice_fiscale"] = st.text_input("Codice Fiscale Coniuge/Partner", value=cliente_data["dati_familiari"]["coniuge"].get("codice_fiscale", ""), key="coniuge_cf")

        # Gestione Figli
        st.markdown("##### Informazioni sui Figli")
        # Il valore del checkbox deve essere persistente nello st.session_state
        has_children_current_value = st.session_state.get("has_children_checkbox", False)
        
        if st.checkbox("Hai figli?", value=has_children_current_value, key="has_children_checkbox"):
            # Se la checkbox viene selezionata, aggiorna lo stato
            if not has_children_current_value: # Se era False e ora è True
                st.session_state.has_children_checkbox = True
                # Inizializza o mostra 1 figlio se prima non ce n'erano
                if not cliente_data["dati_familiari"]["figli"]:
                    cliente_data["dati_familiari"]["figli"].append({})
                    st.session_state.familiari_count = len(cliente_data["dati_familiari"]["figli"]) + len(cliente_data["dati_familiari"]["altri_familiari"])
            
            num_figli = st.number_input("Numero di figli", min_value=0, step=1, value=len(cliente_data["dati_familiari"]["figli"]), key="num_figli_input")
            
            # Assicurati che la lista abbia la dimensione giusta
            while len(cliente_data["dati_familiari"]["figli"]) < num_figli:
                cliente_data["dati_familiari"]["figli"].append({})
            while len(cliente_data["dati_familiari"]["figli"]) > num_figli:
                cliente_data["dati_familiari"]["figli"].pop()

            for i in range(int(num_figli)):
                with st.expander(f"Dati Figlio #{i+1}", expanded=True):
                    figlio = cliente_data["dati_familiari"]["figli"][i]
                    figlio["nome"] = st.text_input(f"Nome Figlio #{i+1}", key=f"figlio_nome_{i}", value=figlio.get('nome', ''))
                    
                    figlio_data_nascita_val = None
                    if figlio.get("data_nascita"):
                        try:
                            figlio_data_nascita_val = datetime.fromisoformat(figlio["data_nascita"]).date()
                        except ValueError:
                            figlio_data_nascita_val = date.today()
                    else:
                        figlio_data_nascita_val = date.today()
                    figlio["data_nascita"] = st.date_input(f"Data di Nascita Figlio #{i+1}", value=figlio_data_nascita_val, key=f"figlio_nascita_{i}").isoformat()
                    
                    figlio["codice_fiscale"] = st.text_input(f"Codice Fiscale Figlio #{i+1}", key=f"figlio_cf_{i}", value=figlio.get('codice_fiscale', ''))
        else:
            # Se la checkbox viene deselezionata, resetta lo stato e la lista figli
            if has_children_current_value: # Se era True e ora è False
                st.session_state.has_children_checkbox = False
                cliente_data["dati_familiari"]["figli"] = [] # Resetta se deselezionato
                st.session_state.familiari_count = len(cliente_data["dati_familiari"]["altri_familiari"]) # Aggiorna il contatore per la dashboard

        # Gestione Altri Familiari a Carico
        st.markdown("##### Altri Familiari a Carico")
        
        # Aggiungo un contatore per la lista, per evitare problemi con la rimozione
        if "altri_familiari_temp_count" not in st.session_state:
            st.session_state.altri_familiari_temp_count = len(cliente_data["dati_familiari"]["altri_familiari"])

        if st.button("➕ Aggiungi Familiare a Carico", key="add_familiare_carico_btn"):
            cliente_data["dati_familiari"]["altri_familiari"].append({})
            st.session_state.altri_familiari_temp_count = len(cliente_data["dati_familiari"]["altri_familiari"])
            # Aggiorna il contatore totale per la dashboard
            st.session_state.familiari_count = len(cliente_data["dati_familiari"]["figli"]) + len(cliente_data["dati_familiari"]["altri_familiari"])

        # Itera sulla lista di familiari a carico per visualizzarli e modificarli
        for i, familiare in enumerate(cliente_data["dati_familiari"]["altri_familiari"]):
            with st.expander(f"Dati Familiare a Carico #{i+1}", expanded=True):
                familiare["nome"] = st.text_input(f"Nome Familiare #{i+1}", key=f"alt_fam_nome_{i}", value=familiare.get('nome', ''))
                familiare["relazione"] = st.text_input(f"Relazione (es. Genitore, Fratello) #{i+1}", key=f"alt_fam_rel_{i}", value=familiare.get('relazione', ''))
                familiare["codice_fiscale"] = st.text_input(f"Codice Fiscale Familiare #{i+1}", key=f"alt_fam_cf_{i}", value=familiare.get('codice_fiscale', ''))
                
                # Bottone di rimozione
                if st.button(f"🗑️ Rimuovi Familiare #{i+1}", key=f"remove_alt_fam_{i}"):
                    cliente_data["dati_familiari"]["altri_familiari"].pop(i)
                    st.session_state.altri_familiari_temp_count = len(cliente_data["dati_familiari"]["altri_familiari"])
                    st.session_state.familiari_count = len(cliente_data["dati_familiari"]["figli"]) + len(cliente_data["dati_familiari"]["altri_familiari"])
                    st.rerun() # Forza un refresh per rimuovere il familiare immediatamente

    # Aggiorna il contatore totale dei familiari per la dashboard (ogni volta che la sezione viene renderizzata)
    st.session_state.familiari_count = len(cliente_data["dati_familiari"]["figli"]) + len(cliente_data["dati_familiari"]["altri_familiari"])
    if cliente_data["dati_personali"].get("stato_civile") in ["Coniugato/a", "Unito Civilmente"] and cliente_data["dati_familiari"]["coniuge"].get("nome_cognome"):
        st.session_state.familiari_count += 1 # Conto anche il coniuge


    # --- Sezione Profilo Finanziario / Segmentazione ---
    with st.expander("Profilo Finanziario e Necessità", expanded=False):
        st.subheader("Informazioni per la Segmentazione")
        
        cliente_data["profilo_finanziario"]["professione"] = st.text_input("Professione / Settore Lavorativo", value=cliente_data["profilo_finanziario"].get("professione", ""), key="cliente_professione")
        cliente_data["profilo_finanziario"]["reddito_annuo_lordo"] = st.number_input("Reddito Annuo Lordo (€)", min_value=0.0, step=1000.0, value=cliente_data["profilo_finanziario"].get("reddito_annuo_lordo", 0.0), key="cliente_reddito")
        
        propensione_rischio_options = ["", "Molto Bassa", "Bassa", "Media", "Alta", "Molto Alta"]
        propensione_rischio_index = propensione_rischio_options.index(cliente_data["profilo_finanziario"].get("propensione_rischio", "")) if cliente_data["profilo_finanziario"].get("propensione_rischio", "") in propensione_rischio_options else 0
        cliente_data["profilo_finanziario"]["propensione_rischio"] = st.selectbox("Propensione al Rischio per Investimenti", propensione_rischio_options, index=propensione_rischio_index, key="cliente_rischio")
        
        st.markdown("##### Aree di Interesse per Consulenza")
        interessi_options = [
            "Pianificazione Previdenziale", "Gestione Investimenti", "Protezione (Assicurazioni)",
            "Pianificazione Successoria", "Consulenza Fiscale", "Finanziamenti/Mutui", "Pianificazione Patrimoniale Generale"
        ]
        
        # Recupera gli interessi selezionati precedentemente
        selected_interessi = cliente_data["profilo_finanziario"].get("aree_interesse", [])
        new_selected_interessi = []
        for interesse in interessi_options:
            checked = st.checkbox(interesse, value=interesse in selected_interessi, key=f"interesse_{interesse.replace(' ', '_').replace('/', '_')}")
            if checked:
                new_selected_interessi.append(interesse)
        cliente_data["profilo_finanziario"]["aree_interesse"] = new_selected_interessi

    st.markdown("---")
    st.info("I dati vengono salvati automaticamente mentre li inserisci.")
