import streamlit as st
from docx import Document
from datetime import date
from io import BytesIO

st.set_page_config(page_title="Consulenza Patrimoniale - Studio Dainotti", layout="wide")
st.title("Scheda Consulenza Patrimoniale - Studio Dainotti")

def init_state():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "familiari" not in st.session_state:
        st.session_state.familiari = []
    if "figli" not in st.session_state:
        st.session_state.figli = []

init_state()

# STEP 0 - Famiglia
if st.session_state.step == 0:
    st.header("🏠 Famiglia e situazione personale")
    nome = st.text_input("Nome e cognome")
    st.session_state.responses["Nome e cognome"] = nome
    st.session_state.responses["Data e luogo di nascita"] = st.text_input("Data e luogo di nascita")
    st.session_state.responses["Codice fiscale"] = st.text_input("Codice fiscale")
    st.session_state.responses["Indirizzo"] = st.text_input("Indirizzo")
    stato_civile = st.selectbox("Stato civile", ["", "Celibe/Nubile", "Coniugato/a", "Separato/a", "Divorziato/a", "Vedovo/a"])
    st.session_state.responses["Stato civile"] = stato_civile

    coniuge_nome = ""
    if stato_civile == "Coniugato/a":
        coniuge_nome = st.text_input("Nome e cognome del coniuge")
        st.session_state.responses["Coniuge"] = coniuge_nome

    ha_figli = st.checkbox("Hai figli?")
    figli = []
    if ha_figli:
        num_figli = st.number_input("Quanti figli vuoi inserire?", min_value=1, step=1)
        for i in range(int(num_figli)):
            with st.expander(f"Figlio #{i+1}"):
                nome_figlio = st.text_input(f"Nome figlio #{i+1}", key=f"figlio_nome_{i}")
                st.session_state.figli.append(nome_figlio)
                nascita = st.text_input(f"Data di nascita figlio #{i+1}", key=f"figlio_nascita_{i}")
                codice = st.text_input(f"Codice fiscale figlio #{i+1}", key=f"figlio_cf_{i}")
                figli.append(f"{nome_figlio} - {nascita} - {codice}")
    st.session_state.responses["Figli"] = figli

    if "familiari_count" not in st.session_state:
        st.session_state.familiari_count = 0

    if st.button("➕ Aggiungi familiare a carico"):
        st.session_state.familiari_count += 1

    familiari_input = []
    for i in range(st.session_state.familiari_count):
        with st.expander(f"Familiare a carico #{i+1}"):
            parentela = st.selectbox(f"Parentela #{i+1}", ["Genitore", "Fratello/Sorella", "Altro"], key=f"parentela_{i}")
            nome_fam = st.text_input(f"Nome familiare #{i+1}", key=f"fam_nome_{i}")
            nascita = st.text_input(f"Data di nascita #{i+1}", key=f"fam_nascita_{i}")
            codice = st.text_input(f"Codice fiscale #{i+1}", key=f"fam_cf_{i}")
            note = st.text_area(f"Note #{i+1}", key=f"fam_note_{i}")
            familiari_input.append(f"{parentela}: {nome_fam} - {nascita} - {codice}. Note: {note}")
            st.session_state.familiari.append(nome_fam)
    st.session_state.responses["Altri familiari a carico"] = familiari_input

    col1, col2 = st.columns([8, 2])
    with col2:
        st.markdown("""
            <style>
            .stButton>button {
                width: 100%;
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 0.75em;
                margin-top: 1em;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("Prosegui ➡️"):
            st.session_state.step = 1

# STEP 1 - Patrimonio
if st.session_state.step >= 1:
    st.header("💼 Area patrimoniale")
    if "patrimonio_count" not in st.session_state:
        st.session_state.patrimonio_count = 0
        st.session_state.patrimonio_voci = []

    if st.button("➕ Aggiungi voce patrimoniale"):
        st.session_state.patrimonio_count += 1

    patrimonio = []
    nomi_possibili = [st.session_state.responses.get("Nome e cognome", "")] + st.session_state.figli + st.session_state.familiari
    if "Coniuge" in st.session_state.responses:
        nomi_possibili.append(st.session_state.responses["Coniuge"])

    for i in range(st.session_state.patrimonio_count):
        with st.expander(f"Voce patrimoniale #{i+1}"):
            tipo = st.selectbox(f"Tipo di patrimonio #{i+1}", [
                "Immobile", "Conto corrente", "Fondo comune", "ETF", "Trust", "Polizza vita", "Quota aziendale", "Altro"
            ], key=f"tipo_patr_{i}")
            descrizione = st.text_input(f"Descrizione sintetica #{i+1}", key=f"desc_patr_{i}")
            intestatario = st.selectbox(f"Intestatario #{i+1}", nomi_possibili, key=f"intestatario_patr_{i}")
            note = st.text_area(f"Note o dettagli aggiuntivi #{i+1}", key=f"note_patr_{i}")

            if tipo in ["Conto corrente", "Fondo comune", "ETF", "Trust", "Polizza vita", "Quota aziendale"]:
                valore = st.number_input(f"Valore stimato in euro #{i+1}", min_value=0.0, step=1000.0, key=f"valore_patr_{i}")
                riga = f"{tipo} - {descrizione} | Valore: {valore:.2f} € | Intestatario: {intestatario} | Note: {note}"
            else:
                riga = f"{tipo} - {descrizione} | Intestatario: {intestatario} | Note: {note}"
            patrimonio.append(riga)

    st.session_state.responses["Patrimonio dettagliato"] = patrimonio

    col1, col2 = st.columns([8, 2])
    with col2:
        st.markdown("""
            <style>
            .stButton>button {
                width: 100%;
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 0.75em;
                margin-top: 1em;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("Prosegui ➡️", key="prosegui_step1"):
            st.session_state.step = 2

# STEP 2 - Pianificazione successoria
if st.session_state.step >= 2:
    st.header("⚖️ Pianificazione successoria e protezione")
    campi = [
        "Nome erede, data nascita, parentela, situazione patrimoniale, note",
        "Donazioni previste", "Beni da destinare specificamente", "Diritti da riservare",
        "Testamento previsto", "Obiettivo evitare conflitti", "Testamento esistente",
        "Donazioni già effettuate", "Clausole o intestazioni", "Trust o fondi patrimoniali", "Quote aziendali"
    ]
    for campo in campi:
        risposta = st.text_area(campo)
        st.session_state.responses[campo] = risposta

    col1, col2 = st.columns([8, 2])
    with col2:
        st.markdown("""
            <style>
            .stButton>button {
                width: 100%;
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 0.75em;
                margin-top: 1em;
            }
            </style>
        """, unsafe_allow_html=True)
        if st.button("Fine o esporta documento"):
            st.session_state.step = 3
