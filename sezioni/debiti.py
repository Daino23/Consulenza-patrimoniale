import streamlit as st

def sezione_debiti():
    st.header("💳 Debiti ricorrenti")

    if st.button("➕ Aggiungi debito"):
        st.session_state.debiti_count += 1

    debiti = []
    for i in range(st.session_state.debiti_count):
        with st.expander(f"Debito #{i+1}"):
            tipo = st.text_input(f"Tipo #{i+1}", key=f"deb_tipo_{i}")
            importo = st.number_input(f"Importo mensile € #{i+1}", min_value=0.0, step=10.0, key=f"deb_importo_{i}")
            debiti.append(f"{tipo} - {importo:.2f} € / mese")

    st.session_state["Debiti ricorrenti"] = debiti
