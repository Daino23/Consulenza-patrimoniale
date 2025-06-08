import streamlit as st
import pandas as pd
from io import BytesIO

def sezione_documenti():
    st.subheader("📄 Generazione Documenti")
    st.write("Genera un file Excel con i dati inseriti nelle altre sezioni.")

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Recupera i dati da st.session_state, ora sono dizionari o liste di dizionari
        
        # Dati Cliente Anagrafica (cliente_anagrafica.py)
        if 'cliente_data' in st.session_state and st.session_state.cliente_data:
            df_cliente_personale = pd.DataFrame([st.session_state.cliente_data['dati_personali']])
            df_cliente_personale.to_excel(writer, index=False, sheet_name="Cliente_DatiPersonali")

            df_cliente_profilo = pd.DataFrame([st.session_state.cliente_data['profilo_finanziario']])
            df_cliente_profilo.to_excel(writer, index=False, sheet_name="Cliente_ProfiloFin")

            if st.session_state.cliente_data['dati_familiari'].get('coniuge'):
                df_coniuge = pd.DataFrame([st.session_state.cliente_data['dati_familiari']['coniuge']])
                df_coniuge.to_excel(writer, index=False, sheet_name="Cliente_Coniuge")
            
            if st.session_state.cliente_data['dati_familiari'].get('figli'):
                df_figli = pd.DataFrame(st.session_state.cliente_data['dati_familiari']['figli'])
                df_figli.to_excel(writer, index=False, sheet_name="Cliente_Figli")
            
            if st.session_state.cliente_data['dati_familiari'].get('altri_familiari'):
                df_altri_fam = pd.DataFrame(st.session_state.cliente_data['dati_familiari']['altri_familiari'])
                df_altri_fam.to_excel(writer, index=False, sheet_name="Cliente_AltriFamiliari")

        # Dati Patrimonio (da lista di dizionari)
        if st.session_state.get("beni_patrimoniali"):
            df_patrimonio = pd.DataFrame(st.session_state.beni_patrimoniali)
            df_patrimonio.to_excel(writer, index=False, sheet_name="Patrimonio")

        # Dati Debiti (da lista di dizionari)
        if st.session_state.get("lista_debiti"):
            df_debiti = pd.DataFrame(st.session_state.lista_debiti)
            df_debiti.to_excel(writer, index=False, sheet_name="Debiti")

        # Dati Obiettivi (da lista di dizionari)
        if st.session_state.get("lista_obiettivi"):
            df_obiettivi = pd.DataFrame(st.session_state.lista_obiettivi)
            df_obiettivi.to_excel(writer, index=False, sheet_name="Obiettivi")
            
    if st.button("📥 Scarica Riepilogo Completo in Excel"):
        output.seek(0)
        st.download_button(
            label="Clicca per Scaricare l'Excel",
            data=output,
            file_name="riepilogo_consulenza.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Contenuto del file: sezioni/documenti.py

import streamlit as st
import pandas as pd
from io import BytesIO
import base64 # Necessario per il download di file (se non già presente)

def sezione_documenti():
    st.subheader("📄 Generazione Documenti")
    st.write("Genera un file Excel con i dati numerici inseriti nelle altre sezioni.")

    # Esempio di dati numerici di esempio. In futuro raccoglieremo quelli reali da session_state.
    # Questo recupero dei dati è generico, assicurati che le chiavi in session_state corrispondano
    # ai nomi effettivi delle liste o dei dizionari salvati dalle altre sezioni.
    # Per Anagrafica Cliente, si userà st.session_state.cliente_data
    # Per Patrimonio, Debiti, Obiettivi, si useranno le liste che contengono i dettagli
    # es: st.session_state.get("patrimonio_list_details", []) se salvi lì i dati dettagliati.
    # Altrimenti, dovresti iterare su st.session_state.patrimonio_count per recuperare i singoli input.

    # Adattamento per recuperare i dati come salvati nelle sezioni (es. da cliente_anagrafica.py)
    # E' un po' più complesso recuperare i dati dettagliati dalle liste dinamiche come patrimonio, debiti, obiettivi
    # perché sono salvati come stringhe per la visualizzazione.
    # Per una vera esportazione, dovremmo salvare i dati strutturati (es. liste di dizionari) e non solo stringhe.
    # Per ora, useremo i dati che sono già accessibili e aggiungeremo un placeholder per gli altri.

    # Dati da Anagrafica Cliente
    cliente_data = st.session_state.get("cliente_data", {})
    dati_personali_cliente = cliente_data.get("dati_personali", {})
    dati_familiari_cliente = cliente_data.get("dati_familiari", {})

    # Dati da Patrimonio, Debiti, Obiettivi (se salvati come liste di dizionari o strutturati)
    # Se le tue sezioni Patrimonio, Debiti, Obiettivi salvano solo stringhe aggregate,
    # qui dovrai recuperare i singoli campi come nell'esempio.
    # Assumiamo che le sezioni salvino i dati come liste di dizionari per una migliore esportazione.
    # Esempio:
    # `patrimonio_items = st.session_state.get("patrimonio_items", [])` (se salvati in questo modo)
    # Vado a prendere i dati come attualmente generati nei tuoi file:
    patrimonio_values = []
    for i in range(st.session_state.get('patrimonio_count', 0)):
        try: # Try-except per gestire chiavi mancanti se l'utente non ha inserito tutto
            tipo = st.session_state[f"tipo_{i}"]
            descrizione = st.session_state[f"desc_{i}"]
            intestatario = st.session_state[f"intest_{i}"]
            valore = st.session_state[f"valore_{i}"]
            patrimonio_values.append({"Tipo": tipo, "Descrizione": descrizione, "Intestatario": intestatario, "Valore": valore})
        except KeyError:
            pass # Skip if data is incomplete

    debiti_values = []
    for i in range(st.session_state.get('debiti_count', 0)):
        try:
            tipo = st.session_state[f"deb_tipo_{i}"]
            importo = st.session_state[f"deb_importo_{i}"]
            debiti_values.append({"Tipo": tipo, "Importo Mensile": importo})
        except KeyError:
            pass

    obiettivi_values = []
    for i in range(st.session_state.get('obiettivi_count', 0)):
        try:
            descrizione = st.session_state[f"ob_desc_{i}"]
            importo = st.session_state[f"ob_importo_{i}"]
            tempo = st.session_state[f"ob_tempo_{i}"]
            obiettivi_values.append({"Descrizione": descrizione, "Importo Target": importo, "Tempo Previsto": tempo})
        except KeyError:
            pass


    if st.button("📥 Scarica riepilogo in Excel"):
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

        output.seek(0)
        st.download_button(
            label="Clicca qui per scaricare",
            data=output.getvalue(),
            file_name="riepilogo_cliente.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
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

    result = 0
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
                result = "Non definito"
        st.success(f"Risultato: {result:.2f}") # Formatta il risultato a due decimali
        st.session_state["calc_result"] = result # Salva il risultato per persistenza nella sessione

    # Mostra il risultato persistente se già calcolato
    if "calc_result" in st.session_state:
        st.write(f"Ultimo Risultato Calcolato: {st.session_state['calc_result']:.2f}")
    else:
        st.info("Nessun dato da scaricare ancora. Compila le sezioni!")
