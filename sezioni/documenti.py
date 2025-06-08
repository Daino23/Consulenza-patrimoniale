import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime # Necessario per datetime.fromisoformat

def sezione_documenti():
    st.subheader("📄 Generazione Documenti")
    st.write("Genera un file Excel con i dati inseriti nelle altre sezioni.")

    # --- Prepara i dati da esportare recuperandoli da st.session_state ---
    cliente_data = st.session_state.get("cliente_data", {})
    dati_personali_cliente = cliente_data.get("dati_personali", {})
    dati_familiari_cliente = cliente_data.get("dati_familiari", {})
    profilo_finanziario_cliente = cliente_data.get("profilo_finanziario", {})

    patrimonio_values = []
    for i in range(st.session_state.get('patrimonio_count', 0)):
        try:
            tipo = st.session_state.get(f"tipo_{i}", "N/A")
            descrizione = st.session_state.get(f"desc_{i}", "N/A")
            intestatario = st.session_state.get(f"intest_{i}", "N/A")
            valore = st.session_state.get(f"valore_{i}", 0.0)
            patrimonio_values.append({"Tipo": tipo, "Descrizione": descrizione, "Intestatario": intestatario, "Valore": valore})
        except Exception:
            pass

    debiti_values = []
    for i in range(st.session_state.get('debiti_count', 0)):
        try:
            tipo = st.session_state.get(f"deb_tipo_{i}", "N/A")
            importo = st.session_state.get(f"deb_importo_{i}", 0.0)
            debiti_values.append({"Tipo": tipo, "Importo Mensile": importo})
        except Exception:
            pass

    obiettivi_values = []
    for i in range(st.session_state.get('obiettivi_count', 0)):
        try:
            descrizione = st.session_state.get(f"ob_desc_{i}", "N/A")
            importo = st.session_state.get(f"ob_importo_{i}", 0.0)
            tempo = st.session_state.get(f"ob_tempo_{i}", "N/A")
            obiettivi_values.append({"Descrizione": descrizione, "Importo Target": importo, "Tempo Previsto": tempo})
        except Exception:
            pass
    
    # Dati da CRM (se presenti)
    crm_clients = st.session_state.get("crm_clients", [])


    # --- Logica per la generazione e il download del file Excel ---
    # Controlla se ci sono dati significativi prima di generare l'Excel
    if dati_personali_cliente or patrimonio_values or debiti_values or obiettivi_values or crm_clients:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Scheda Dati Anagrafici
            if dati_personali_cliente:
                df_anagrafica = pd.DataFrame([dati_personali_cliente])
                df_anagrafica.to_excel(writer, index=False, sheet_name="Anagrafica Cliente")

            # Scheda Dati Familiari
            if dati_familiari_cliente:
                familiari_list = []
                if dati_familiari_cliente.get("coniuge"):
                    familiari_list.append({"Tipo": "Coniuge", **dati_familiari_cliente["coniuge"]})
                if dati_familiari_cliente.get("figli"):
                    for i, figlio in enumerate(dati_familiari_cliente["figli"]):
                        familiari_list.append({"Tipo": f"Figlio {i+1}", **figlio})
                if dati_familiari_cliente.get("altri_familiari"):
                    for i, alt_fam in enumerate(dati_familiari_cliente["altri_familiari"]):
                        familiari_list.append({"Tipo": f"Altro Familiare {i+1}", **alt_fam})
                if familiari_list:
                    df_familiari = pd.DataFrame(familiari_list)
                    df_familiari.to_excel(writer, index=False, sheet_name="Composizione Familiare")
            
            # Scheda Profilo Finanziario
            if profilo_finanziario_cliente:
                df_profilo_finanziario = pd.DataFrame([profilo_finanziario_cliente])
                df_profilo_finanziario.to_excel(writer, index=False, sheet_name="Profilo Finanziario")

            # Scheda Patrimonio
            if patrimonio_values:
                df_pat = pd.DataFrame(patrimonio_values)
                df_pat.to_excel(writer, index=False, sheet_name="Patrimonio")

            # Scheda Debiti
            if debiti_values:
                df_deb = pd.DataFrame(debiti_values)
                df_deb.to_excel(writer, index=False, sheet_name="Debiti")

            # Scheda Obiettivi
            if obiettivi_values:
                df_obi = pd.DataFrame(obiettivi_values)
                df_obi.to_excel(writer, index=False, sheet_name="Obiettivi")
            
            # Scheda Clienti CRM
            if crm_clients:
                # Per i clienti CRM, potremmo voler esportare anche le interazioni
                # ma per ora esportiamo solo i dati principali dei clienti
                crm_df_data = []
                for client in crm_clients:
                    client_copy = client.copy()
                    client_copy.pop('interactions', None) # Rimuove le interazioni per la tabella principale
                    crm_df_data.append(client_copy)
                
                df_crm_clients = pd.DataFrame(crm_df_data)
                df_crm_clients.to_excel(writer, index=False, sheet_name="CRM_Clienti")

                # Volendo, si potrebbe creare una scheda separata per tutte le interazioni
                all_interactions = []
                for client in crm_clients:
                    for interaction in client.get('interactions', []):
                        interaction_copy = interaction.copy()
                        interaction_copy['Client_Name'] = client['name'] # Aggiungi il nome del cliente
                        all_interactions.append(interaction_copy)
                if all_interactions:
                    df_crm_interactions = pd.DataFrame(all_interactions)
                    df_crm_interactions.to_excel(writer, index=False, sheet_name="CRM_Interazioni")


        output.seek(0) # Riporta il cursore all'inizio del buffer
        st.download_button(
            label="📥 Scarica Riepilogo Completo in Excel",
            data=output.getvalue(), # È fondamentale usare .getvalue() per ottenere i byte
            file_name="riepilogo_consulenza.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Nessun dato significativo da scaricare ancora. Compila le sezioni Anagrafica Cliente, Patrimonio, Debiti, Obiettivi o CRM.")

    st.markdown("---") # Linea separatrice

    # --- Sezione Calcolatrice ---
    st.subheader("🧮 Calcolatrice Rapida")
    st.markdown("Esegui calcoli semplici direttamente qui.")

    col_calc1, col_calc2 = st.columns(2)

    with col_calc1:
        num1 = st.number_input("Primo Numero", value=0.0, format="%.2f", key="calc_num1")
    with col_calc2:
        num2 = st.number_input("Secondo Numero", value=0.0, format="%.2f", key="calc_num2")

    operation = st.selectbox("Seleziona Operazione", ["+", "-", "*", "/"], key="calc_op")

    # Inizializza il risultato della calcolatrice se non esiste
    if "calc_result" not in st.session_state:
        st.session_state["calc_result"] = 0.0

    if st.button("Calcola", key="calc_button"):
        if operation == "+":
            st.session_state["calc_result"] = num1 + num2
        elif operation == "-":
            st.session_state["calc_result"] = num1 - num2
        elif operation == "*":
            st.session_state["calc_result"] = num1 * num2
        elif operation == "/":
            if num2 != 0:
                st.session_state["calc_result"] = num1 / num2
            else:
                st.error("Errore: Divisione per zero!")
                st.session_state["calc_result"] = "Non definito" # Gestisce l'errore nel risultato
        
        # Mostra il risultato subito dopo il calcolo
        if isinstance(st.session_state["calc_result"], (float, int)):
            st.success(f"Risultato: {st.session_state['calc_result']:.2f}")
        else:
            st.success(f"Risultato: {st.session_state['calc_result']}") # Per "Non definito"
        st.rerun() # Forza il refresh per aggiornare il risultato persistente

    # Mostra l'ultimo risultato calcolato (persistente nella sessione)
    if isinstance(st.session_state["calc_result"], (float, int)):
        st.write(f"Ultimo Risultato Calcolato: **{st.session_state['calc_result']:.2f}**")
    else:
        st.write(f"Ultimo Risultato Calcolato: **{st.session_state['calc_result']}**")
