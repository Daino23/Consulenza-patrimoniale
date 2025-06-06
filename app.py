import streamlit as st
from docx import Document
from datetime import date
from io import BytesIO

st.set_page_config(page_title="Consulenza Patrimoniale - Studio Dainotti", layout="wide")
st.title("Scheda Consulenza Patrimoniale - Studio Dainotti")

# Inizializza lo stato
def init_state():
    if "responses" not in st.session_state:
        st.session_state.responses = {}

init_state()

# Sezioni e domande
sections = {
    "🏠 Famiglia e situazione personale": [
        "Nome e cognome", "Data e luogo di nascita", "Codice fiscale", "Indirizzo", "Stato civile",
        "Coniuge", "Figli", "Altri familiari a carico",
        "Occupazione", "Reddito lordo annuo", "Altri redditi", "Debiti ricorrenti"
    ],
    "💼 Area patrimoniale": [
        "Indirizzo immobile", "Intestatario e quota", "Valore stimato", "Uso", "Mutui o vincoli presenti",
        "Conti correnti", "Investimenti", "Polizze vita", "Fondi pensione",
        "Debiti personali", "Fideiussioni", "Leasing o finanziamenti"
    ],
    "⚖️ Pianificazione successoria e protezione": [
        "Nome erede, data nascita, parentela, situazione patrimoniale, note",
        "Donazioni previste", "Beni da destinare specificamente", "Diritti da riservare", "Testamento previsto", "Obiettivo evitare conflitti",
        "Testamento esistente", "Donazioni già effettuate", "Clausole o intestazioni", "Trust o fondi patrimoniali", "Quote aziendali"
    ],
    "🔍 Obiettivi e bisogni": [
        "Protezione del patrimonio", "Ottimizzazione fiscale", "Passaggio generazionale", "Altro",
        "Contenziosi", "Fragilità", "Beni all’estero", "Altre criticità"
    ],
    "📎 Allegati richiesti": [
        "Visure catastali", "Atti notarili", "Documentazione assicurativa", "Estratti conto", "Testamenti o donazioni", "Quote societarie"
    ]
}

# Aggiunta di un tab finale per l'esportazione
tab_titles = list(sections.keys()) + ["📄 Esporta documento"]
tabs = st.tabs(tab_titles)

# Tab di compilazione
for i, section in enumerate(sections.keys()):
    with tabs[i]:
        st.header(section)
        for question in sections[section]:
            response = st.text_area(question, key=question)
            st.session_state.responses[question] = response

# Tab finale: esportazione documento
with tabs[-1]:
    st.header("📄 Esporta il documento Word finale")

    if st.button("Genera documento Word"):
        doc = Document()

        # Intestazione
        section = doc.sections[0]
        header = section.header.paragraphs[0]
        header.text = "Studio Dainotti - Consulenza patrimoniale, tributaria e del credito\n" \
                      "Via Roma 52, Porto Valtravaglia (VA) - www.dainotti.com - info@dainotti.com"

        doc.add_paragraph(f"Data compilazione: {date.today().strftime('%d/%m/%Y')}")
        doc.add_heading("Scheda Raccolta Informazioni - Consulenza Patrimoniale", 0)

        for section_title, questions in sections.items():
            doc.add_heading(section_title, level=1)
            for question in questions:
                answer = st.session_state.responses.get(question, "")
                doc.add_paragraph(f"{question}: {answer}")

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.success("Documento generato con successo!")
        st.download_button(
            label="📥 Scarica il file Word",
            data=buffer,
            file_name="Scheda_Consulenza_Patrimoniale.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
