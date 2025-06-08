import streamlit as st
import pandas as pd
from io import BytesIO


def sezione_documenti():
    st.subheader("📄 Generazione Documenti")
    st.write("Genera un file Excel con i dati numerici inseriti nelle altre sezioni.")

    # Esempio di dati numerici di esempio. In futuro raccoglieremo quelli reali da session_state.
    dati_familiari = st.session_state.get("familiari", [])
    dati_patrimonio = st.session_state.get("patrimonio", [])
    dati_debiti = st.session_state.get("debiti", [])
    dati_obiettivi = st.session_state.get("obiettivi", [])

    if st.button("📥 Scarica riepilogo in Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if dati_familiari:
                df_fam = pd.DataFrame(dati_familiari)
                df_fam.to_excel(writer, index=False, sheet_name="Familiari")

            if dati_patrimonio:
                df_pat = pd.DataFrame(dati_patrimonio)
                df_pat.to_excel(writer, index=False, sheet_name="Patrimonio")

            if dati_debiti:
                df_deb = pd.DataFrame(dati_debiti)
                df_deb.to_excel(writer, index=False, sheet_name="Debiti")

            if dati_obiettivi:
                df_obi = pd.DataFrame(dati_obiettivi)
                df_obi.to_excel(writer, index=False, sheet_name="Obiettivi")

        output.seek(0)
        st.download_button(
            label="📥 Clicca qui per scaricare il file Excel",
            data=output,
            file_name="riepilogo_consulenza.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
