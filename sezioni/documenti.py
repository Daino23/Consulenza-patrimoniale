import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime # Necessario per datetime.fromisoformat

def sezione_documenti():
    st.subheader("📄 Generazione Documenti")
    st.write("Genera un file Excel con i dati inseriti nelle altre sezioni.")

    # --- Logica per la preparazione dei dati per l'Excel ---
    # Recupera i dati da st.session_state.
    # Assumiamo che le altre sezioni salvino i dati come liste di dizionari strutturati.

    cliente_data = st.session_state.get('cliente_data', {})
    
    # Verifica se ci sono dati per l'esportazione
    # Almeno una delle sezioni principali deve contenere dati
    has_data_to_export = False
    if cliente_data.get('dati_personali') or \
       (cliente_data.get('dati_familiari') and (cliente_data['dati_familiari'].get('coniuge') or cliente_data['dati_familiari'].get('figli') or cliente_data['dati_familiari'].get('altri_familiari'))):
        has_data_to_export = True
    if st.session_state.get('beni_patrimoniali'):
        has_data_to_export = True
    if st.session_state.get('lista_debiti'):
        has_data_to_export = True
    if st.session_state.get('lista_obiettivi'):
        has_data_to_export = True
    # Aggiungi qui altre condizioni se hai altre sezioni con dati esportabili (es. CRM)


    if has_data_to_export:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Dati Cliente Anagrafica (da cliente_anagrafica.py)
            if cliente_data.get('dati_personali'):
                df_cliente_personale = pd.DataFrame([cliente_data['dati_personali']])
                df_cliente_personale.to_excel(writer, index=False, sheet_name="Cliente_DatiPersonali")

            if cliente_data.get('profilo_finanziario'):
                df_cliente_profilo = pd.DataFrame([cliente_data['profilo_finanziario']])
                df_cliente_profilo.to_excel(writer, index=False, sheet_name="Cliente_ProfiloFin")

            if cliente_data.get('dati_familiari'):
                familiari_list = []
                if cliente_data['dati_familiari'].get('coniuge'):
                    familiari_list.append({"Tipo": "Coniuge", **cliente_data['dati_familiari']['coniuge']})
                if cliente_data['dati_familiari'].get('figli'):
                    for figlio in cliente_data['dati_familiari']['figli']:
                        familiari_list.append({"Tipo": "Figlio", **figlio})
                if cliente_data['dati_familiari'].get('altri_familiari'):
                    for alt_fam in cliente_data['dati_familiari']['altri_familiari']:
                        familiari_list.append({"Tipo": "Altro Familiare", **alt_fam})

                if familiari_list:
                    df_familiari = pd.DataFrame(familiari_list)
                    df_familiari.to_excel(writer, index=False, sheet_name="Cliente_Familiari")

            # Dati Patrimonio (da st.session_state.beni_patrimoniali)
            if st.session_state.get("beni_patrimoniali"):
                df_patrimonio = pd.DataFrame(st.session_state.beni_patrimoniali)
                df_patrimonio.to_excel(writer, index=False, sheet_name="Patrimonio")

            # Dati Debiti (da st.session_state.lista_debiti)
            if st.session_state.get("lista_debiti"):
                df_debiti = pd.DataFrame(st.session_state.lista_debiti)
                df_debiti.to_excel(writer, index=False, sheet_name="Debiti")

            # Dati Obiettivi (da st.session_state.lista_obiettivi)
            if st.session_state.get("lista_obiettivi"):
                df_obiettivi = pd.DataFrame(st.session_state.lista_obiettivi)
                df_obiettivi.to_excel(writer, index=False, sheet_name="Obiettivi")

        output.seek(0) # Riporta il cursore all'inizio del buffer
        st.download_button(
            label="📥 Scarica Riepilogo Completo in Excel",
            data=output.getvalue(), # CORRETTO: usa .getvalue()
            file_name="riepilogo_consulenza.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Nessun dato da scaricare ancora. Compila le sezioni Anagrafica Cliente, Patrimonio, Debiti o Obiettivi!")

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

    result = 0.0 # Inizializza result come float
    if st.button("Calcola", key="calc_button"):
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 != 0:
                result = num1 / num2
            else:
                st.error("Errore: Divisione per zero!")
                result = "Non definito" # Se c'è un errore, il risultato non è numerico

        # Mostra il risultato subito dopo il calcolo
        if isinstance(result, float): # Se il risultato è numerico, formattalo
            st.success(f"Risultato: {result:.2f}")
        else: # Altrimenti, mostra "Non definito" o il messaggio di errore
            st.success(f"Risultato: {result}")

        st.session_state["calc_result"] = result # Salva il risultato per persistenza nella sessione

    # Mostra il risultato persistente se già calcolato
    if "calc_result" in st.session_state and st.session_state["calc_result"] != "Non definito":
        st.write(f"Ultimo Risultato Calcolato: **{st.session_state['calc_result']:.2f}**")
    elif "calc_result" in st.session_state and st.session_state["calc_result"] == "Non definito":
         st.write(f"Ultimo Risultato Calcolato: **{st.session_state['calc_result']}**")
