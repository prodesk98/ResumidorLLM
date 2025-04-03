import uuid

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from llm import get_llm
from utils import PDFParser


client = get_llm()

pdf_text = ""
prompt = None

# Initialize session states
if "chat_id" not in st.session_state:
    st.session_state.chat_id = uuid.uuid4().hex

if "summary" not in st.session_state:
    st.session_state.summary = None

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "current_flashcard" not in st.session_state:
    st.session_state.current_flashcard = 0

if "messages" not in st.session_state:
    st.session_state.messages = []
#

# --- Sidebar ---
with st.sidebar:
    if st.button("➕ Novo"):
        st.session_state.clear()
        st.rerun()

    st.write(f"_{st.session_state.chat_id}_")
    st.markdown("---")

    # Step 0: Upload PDF
    uploaded_file = st.file_uploader("Envie um PDF para extração de texto", type="pdf")

    if uploaded_file is not None:
        try:
            pdf_parser = PDFParser(uploaded_file.read())
            pdf_text = pdf_parser.to_text()
            if st.button("Analisar PDF"):
                prompt = pdf_text
                pdf_text = ""
                uploaded_file = None
        except Exception as e:
            st.error(f"Erro ao ler o PDF: {e}")


#

# Optional manual input
manual_prompt = st.chat_input("Digite seu texto...")

if manual_prompt:
    prompt = manual_prompt

# Step 2: Generate Summary
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        st.session_state.summary = None
        st.session_state.flashcards = []
        st.session_state.current_flashcard = 0
        with st.spinner("Agentes gerando resumo..."):
            # Placeholder for feedback
            feedback_placeholder = st.empty()
            agent_output = client.generate(
                [
                    HumanMessage(content=m['content'])
                    if m['role'] == "user"
                    else AIMessage(
                        content=m['content'],
                        additional_kwargs={"name": m['role']}
                    )
                    for m in st.session_state.messages
                ],
                placeholder=feedback_placeholder,
            )
            st.session_state.summary = agent_output
            st.session_state.messages.append({"role": "assistant", "content": agent_output})
            st.success("✅ Concluído!")

            if len(st.session_state.summary) >= 900:
                st.subheader("Flashcards: Crie flashcards para fixar o conteúdo.")

                quantities = st.number_input(
                    "Quantas flashcards você gostaria de gerar?",
                    min_value=1,
                    max_value=10,
                    value=5,
                )

                if st.button("Criar Flashcards"):
                    with st.spinner(f"Gerando {quantities} flashcards..."):
                        try:
                            flashcards = client.flashcard(st.session_state.summary, quantities)

                            if isinstance(flashcards, list) and len(flashcards) > 0:
                                st.session_state.flashcards = flashcards
                                st.session_state.current_flashcard = 0
                                st.success(f"{len(flashcards)} Flashcards criados com sucesso!")
                            else:
                                st.warning("Nenhum flashcard foi gerado.")
                        except Exception as e:
                            st.error(f"Erro ao gerar flashcards: {e}")

                if st.button("Salvar"):
                    st.success("Resumo salvo com sucesso!")

            # Write the summary
            st.write(st.session_state.summary)


# Step 4: Flashcard Viewer
if st.session_state.flashcards:
    current_index = st.session_state.current_flashcard
    current_card = st.session_state.flashcards[current_index]

    st.subheader(f"Flashcard {current_index + 1} de {len(st.session_state.flashcards)}")

    if st.button("Mostrar Pergunta"):
        st.write(current_card.question)

    if st.button("Mostrar Resposta"):
        st.success(current_card.answer)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Voltar", disabled=current_index == 0):
            st.session_state.current_flashcard -= 1
    with col2:
        if st.button("Próximo", disabled=current_index == len(st.session_state.flashcards) - 1):
            st.session_state.current_flashcard += 1
