import streamlit as st
from datetime import datetime

# Titolo e introduzione
st.set_page_config(page_title="Dashboard Consulente - Studio Dainotti", layout="wide")
st.title("📊 Dashboard Consulente")
st.markdown("Benvenuto nella tua area di controllo. Da qui puoi accedere rapidamente a tutti i tuoi strumenti.")

# Layout a colonne per riepilogo e navigazione
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("📅 Oggi è")
    st.markdown(f"### {datetime.now().strftime('%d/%m/%Y')} 🕒 {datetime.now().strftime('%H:%M')}")

    st.subheader("📂 Accessi rapidi")
    if st.button("👨‍👩‍👧 Famiglia e situazione personale"):
        st.switch_page("/app.py")
    if st.button("🏦 Patrimonio"):
        st.switch_page("/app.py")
    if st.button("💳 Debiti"):
        st.switch_page("/app.py")
    if st.button("🎯 Obiettivi"):
        st.switch_page("/app.py")
    if st.button("📁 Documenti"):
        st.switch_page("/app.py")

with col2:
    st.subheader("🔔 Prossime attività")
    st.markdown("- [ ] Chiamata con cliente Rossi - 10:30\n- [ ] Inviare report consulenza Bianchi\n- [ ] Completare inserimento pratica mutuo Verdi")

    st.subheader("📌 Note rapide")
    note = st.text_area("Scrivi una nota rapida...", height=100)
    if st.button("Salva nota"):
        st.success("Nota salvata (non persiste al riavvio: sistema temporaneo)")

# Avviso fine
st.markdown("---")
st.markdown("© Studio Dainotti - Tutti i diritti riservati")
