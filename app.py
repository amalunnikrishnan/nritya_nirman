import streamlit as st
from project import CompositionType, generate_composition

COMPOSITION_TYPES = {
    "तिहाई": CompositionType.TIHAI,
    "टुकड़ा": CompositionType.TUKDA,
    "चक्करदार टुकड़ा": CompositionType.CHAKKARDAR,
    "सम-से-सम टुकड़ा": CompositionType.SAM_SE_SAM,
}


def generate():
    composition_type = COMPOSITION_TYPES.get(st.session_state.get("composition_type"))
    if not composition_type:
        return
    st.session_state.composition_latin = st.session_state.get("composition_latin", "")
    st.session_state.composition_devanagari = st.session_state.get(
        "composition_devanagari", ""
    )
    composition = generate_composition(composition_type=composition_type)
    if composition:
        st.session_state.composition_latin = str(composition)
        st.session_state.composition_devanagari = str(composition.transliterated())


st.session_state.composition_latin = st.session_state.get("composition_latin", "")
st.session_state.composition_devanagari = st.session_state.get(
    "composition_devanagari", ""
)

sidebar, main = st.columns([1, 1])

sidebar.image("outline.png", width=200)
sidebar.title("नृत्य निर्माण")


def select_composition_type(index: int):
    st.session_state.composition_type = index


sidebar.selectbox(
    "Composition type",
    key="composition_type",
    options=COMPOSITION_TYPES.keys(),
)

# st.text_area("Description", key="description")

sidebar.button(
    "Generate Composition",
    on_click=lambda: generate(),
)

# st.write(st.session_state.composition_latin)
main.write(st.session_state.composition_devanagari)
