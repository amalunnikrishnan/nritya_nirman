import streamlit as st
from project import user_proxy, manager
from composition_parser import get_composition_parser, Composition

COMPOSITION_TYPES = {
    "तिहाई": "Tihai",
    "तुकड़ा": "Tukda",
    "चक्करदार": "Chakkardar",
    "सम-से-सम": "Sam-se-sam",
}


def generate():
    composition_type = COMPOSITION_TYPES.get(st.session_state.get("composition_type"))
    if not composition_type:
        return
    description = st.session_state.get("description")
    message = f"Generate a {composition_type}."
    if description:
        message += f" {description}"
    chat_result = user_proxy.initiate_chat(manager, message=message)
    parser = get_composition_parser()
    st.session_state.composition_latin = st.session_state.get("composition_latin", "")
    st.session_state.composition_devanagari = st.session_state.get(
        "composition_devanagari", ""
    )
    for message in chat_result.chat_history[::-1]:
        composition = parser.invoke(message["content"])
        if (
            composition
            and isinstance(composition, Composition)
            and composition.is_valid()
        ):
            print(composition)
            st.session_state.composition_latin = str(composition)
            st.session_state.composition_devanagari = str(composition.transliterated())
            break
        print("Invalid", composition)
        continue


st.session_state.composition_latin = st.session_state.get("composition_latin", "")
st.session_state.composition_devanagari = st.session_state.get(
    "composition_devanagari", ""
)

st.title("नृत्य निर्माण")


def select_composition_type(index: int):
    st.session_state.composition_type = index


st.selectbox(
    "Composition type",
    key="composition_type",
    options=COMPOSITION_TYPES.keys(),
)

# st.text_area("Description", key="description")

st.button(
    "Generate Composition",
    on_click=lambda: generate(),
)

# st.write(st.session_state.composition_latin)
st.write(st.session_state.composition_devanagari)
