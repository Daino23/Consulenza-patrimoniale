import streamlit as st

def sezione_patrimonio():
    st.header("💼 Area patrimoniale")

    if st.button("➕ Aggiungi bene patrimoniale"):
        st.session_state.patrimonio_count += 1

    patrimonio = []
    for i in range(st.session_state.patrimonio_count):
        with st.expander(f"Bene #{i+1}"):
            tipo = st.selectbox(f"Tipo di bene #{i+1}", ["Immobile", "Conto corrente", "Fondo", "ETF", "Trust", "Altro"], key=f"tipo_{i}")
            descrizione = st.text_input(f"Descrizione #{i+1}", key=f"desc_{i}")
            intestatario = st.text_input(f"Intestatario #{i+1}", key=f"intest_{i}")
            valore = st.number_input(f"Valore stimato € #{i+1}", min_value=0.0, step=100.0, key=f"valore_{i}")
            patrimonio.append(f"{tipo} - {descrizione} - {intestatario} - {valore:.2f} €")
    
    st.session_state["Situazione patrimoniale"] = patrimonio
