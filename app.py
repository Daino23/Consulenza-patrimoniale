import streamlit as st
from datetime import date

# Inizializzazione dello stato sessione
if "familiari_count" not in st.session_state:
    st.session_state.familiari_count = 0
if "patrimonio_count" not in st.session_state:
    st.session_state.patrimonio_count = 0

# Funzione principale per eseguire tutte le sezioni

def main():
    st.set_page_config(page_title="Consulenza Patrimoniale - Studio Dainotti", layout="wide")
    st.title("Scheda Consulenza Patrimoniale - Studio Dainotti")

    st.markdown("""
        <style>
        .block-container {
            padding-top: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## Navigazione")
        sezione = st.radio("Vai alla sezione:", ["Famiglia", "Patrimonio"])

    if sezione == "Famiglia":
        sezione_famiglia()
    elif sezione == "Patrimonio":
        sezione_patrimonio()


# Sezione: Famiglia e situazione personale
def sezione_famiglia():
    st.header("\U0001F3E0 Famiglia e situazione personale")
    responses = {}

    col1, col2 = st.columns(2)
    with col1:
        responses["Nome e cognome"] = st.text_input("Nome e cognome")
        responses["Codice fiscale"] = st.text_input("Codice fiscale")
        responses["Indirizzo"] = st.text_input("Indirizzo")
    with col2:
        responses["Data e luogo di nascita"] = st.text_input("Data e luogo di nascita")
        stato_civile = st.selectbox("Stato civile", ["", "Celibe/Nubile", "Coniugato/a", "Separato/a", "Divorziato/a", "Vedovo/a"])
        responses["Stato civile"] = stato_civile

    if stato_civile == "Coniugato/a":
        responses["Coniuge"] = st.text_input("Nome e cognome del coniuge")

    if st.checkbox("Hai figli?"):
        num_figli = st.number_input("Numero di figli", min_value=1, step=1)
        figli = []
        for i in range(int(num_figli)):
            with st.expander(f"Figlio #{i+1}"):
                nome = st.text_input(f"Nome figlio #{i+1}", key=f"figlio_nome_{i}")
                nascita = st.text_input(f"Data di nascita figlio #{i+1}", key=f"figlio_nascita_{i}")
                codice = st.text_input(f"Codice fiscale figlio #{i+1}", key=f"figlio_cf_{i}")
                figli.append(f"{nome} - {nascita} - {codice}")
        responses["Figli"] = figli

    st.subheader("\U0001F46B Altri familiari a carico")
    if st.button("➕ Aggiungi familiare a carico"):
        st.session_state.familiari_count += 1

    familiari = []
    for i in range(st.session_state.familiari_count):
        with st.expander(f"Familiare #{i+1}"):
            nome = st.text_input(f"Nome #{i+1}", key=f"fam_nome_{i}")
            relazione = st.text_input(f"Relazione #{i+1}", key=f"fam_rel_{i}")
            codice = st.text_input(f"Codice fiscale #{i+1}", key=f"fam_cf_{i}")
            familiari.append(f"{nome} ({relazione}) - CF: {codice}")
    responses["Altri familiari a carico"] = familiari

    return responses


# Sezione: Patrimonio
def sezione_patrimonio():
    st.header("\U0001F4BC Area patrimoniale")
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

    return patrimonio


# Avvio dell'app
if __name__ == "__main__":
    main()
