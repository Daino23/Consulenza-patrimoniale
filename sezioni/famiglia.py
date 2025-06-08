import streamlit as st

def sezione_famiglia():
    st.header("\U0001F3E0 Famiglia e situazione personale")

    st.session_state.responses = st.session_state.get("responses", {})

    st.session_state.responses["Nome e cognome"] = st.text_input("Nome e cognome")
    st.session_state.responses["Data e luogo di nascita"] = st.text_input("Data e luogo di nascita")
    st.session_state.responses["Codice fiscale"] = st.text_input("Codice fiscale")
    st.session_state.responses["Indirizzo"] = st.text_input("Indirizzo")

    stato_civile = st.selectbox("Stato civile", ["", "Celibe/Nubile", "Coniugato/a", "Separato/a", "Divorziato/a", "Vedovo/a"])
    st.session_state.responses["Stato civile"] = stato_civile

    if stato_civile == "Coniugato/a":
        st.session_state.responses["Coniuge"] = st.text_input("Nome e cognome del coniuge")

    if st.checkbox("Hai figli?"):
        num_figli = st.number_input("Numero di figli", min_value=1, step=1)
        figli = []
        for i in range(int(num_figli)):
            with st.expander(f"Figlio #{i+1}"):
                nome = st.text_input(f"Nome figlio #{i+1}", key=f"figlio_nome_{i}")
                nascita = st.text_input(f"Data di nascita figlio #{i+1}", key=f"figlio_nascita_{i}")
                codice = st.text_input(f"Codice fiscale figlio #{i+1}", key=f"figlio_cf_{i}")
                figli.append(f"{nome} - {nascita} - {codice}")
        st.session_state.responses["Figli"] = figli

    st.subheader("\U0001F46B Altri familiari a carico")
    if st.button("\u2795 Aggiungi familiare a carico"):
        st.session_state.familiari_count += 1

    familiari = []
    for i in range(st.session_state.familiari_count):
        with st.expander(f"Familiare #{i+1}"):
            nome = st.text_input(f"Nome #{i+1}", key=f"fam_nome_{i}")
            relazione = st.text_input(f"Relazione #{i+1}", key=f"fam_rel_{i}")
            codice = st.text_input(f"Codice fiscale #{i+1}", key=f"fam_cf_{i}")
            familiari.append(f"{nome} ({relazione}) - CF: {codice}")
    st.session_state.responses["Altri familiari a carico"] = familiari
