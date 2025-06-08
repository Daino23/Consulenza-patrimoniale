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
    else:
        st.info("Nessun dato da scaricare ancora. Compila le sezioni!")
