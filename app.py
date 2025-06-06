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
    if "familiari_count" not in st.session_state:
        st.session_state.familiari_count = 0
    if "patrimonio_count" not in st.session_state:
        st.session_state.patrimonio_count = 0
    if "debiti_count" not in st.session_state:
        st.session_state.debiti_count = 0
    if "obiettivi_count" not in st.session_state:
        st.session_state.obiettivi_count = 0

init_state()

custom_button_style = """
    <style>
    .prosegui-button > button {
        width: 100%;
        font-weight: bold;
        padding: 0.75em;
        margin-top: 1em;
        border-radius: 6px;
        border: none;
    }
    </style>
"""

# ... [STEP 0, 1, 2 come sopra] ...

# STEP 3 - Obiettivi economici
if st.session_state.step == 3:
    st.header("\U0001F4C8 Obiettivi economici")

    if st.button("➕ Aggiungi obiettivo"):
        st.session_state.obiettivi_count += 1

    obiettivi = []
    for i in range(st.session_state.obiettivi_count):
        with st.expander(f"Obiettivo #{i+1}"):
            descrizione = st.text_input(f"Descrizione obiettivo #{i+1}", key=f"ob_desc_{i}")
            importo = st.number_input(f"Importo da raggiungere (€) #{i+1}", min_value=0.0, step=500.0, key=f"ob_importo_{i}")
            scadenza = st.text_input(f"Tempo previsto (es. 12 mesi) #{i+1}", key=f"ob_scadenza_{i}")
            obiettivi.append(f"{descrizione} | Importo: {importo:.2f} € | Tempo previsto: {scadenza}")

    st.session_state.responses["Obiettivi economici"] = obiettivi

    col1, col2 = st.columns([8, 2])
    with col2:
        st.markdown(custom_button_style, unsafe_allow_html=True)
        st.markdown('<div class="prosegui-button">', unsafe_allow_html=True)
        if st.button("Prosegui ➡️", key="to_step_4"):
            st.session_state.step = 4
        st.markdown('</div>', unsafe_allow_html=True)

# STEP 4 - Genera Word
if st.session_state.step == 4:
    st.header("\U0001F4C4 Genera documento Word")

    if st.button("Crea documento Word"):
        doc = Document()
        doc.add_heading("Scheda Consulenza Patrimoniale", 0)
        doc.add_paragraph(f"Data: {date.today().strftime('%d/%m/%Y')}")

        for sezione, risposte in st.session_state.responses.items():
            doc.add_heading(sezione, level=1)
            if isinstance(risposte, list):
                for voce in risposte:
                    doc.add_paragraph(str(voce), style='List Bullet')
            else:
                doc.add_paragraph(str(risposte))

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="📥 Scarica documento Word",
            data=buffer,
            file_name="scheda_consulenza_patrimoniale.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
