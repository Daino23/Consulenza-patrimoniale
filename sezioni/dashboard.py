import streamlit as st
from datetime import date

def sezione_dashboard():
    st.header("📊 Dashboard Principale")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Oggi è:")
        st.write(date.today().strftime("%A %d %B %Y"))
    
    with col2:
        st.subheader("Note rapide")
        st.text_area("Scrivi un appunto", "")

    st.divider()
    st.subheader("📌 Sezioni rapide")
    st.markdown("- [ ] Famiglia\n- [ ] Patrimonio\n- [ ] Debiti\n- [ ] Obiettivi\n- [ ] Documenti")
