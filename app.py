import streamlit as st
from project import user_proxy, manager
from composition_parser import get_composition_parser, Composition


def generate():
    composition_type = st.session_state.get("composition_type")
    if not composition_type:
        return
    description = st.session_state.get("description")
    message = f"Generate a {composition_type}."
    if description:
        message += f"\n{description}"
    chat_result = user_proxy.initiate_chat(manager, message=message)
    parser = get_composition_parser()
    for message in chat_result.chat_history[::-1]:
        composition = parser.invoke(message["content"])
        if (
            composition
            and isinstance(composition, Composition)
            and composition.is_valid()
        ):
            print(composition)
            st.session_state.composition = (
                str(composition) + "\n\n" + str(composition.transliterated())
            )
            break
        print("Invalid", composition)
        continue


st.session_state.composition = st.session_state.get("composition", "")

st.title("Nritya Nirman")
COMPOSITION_TYPES = ["Tihai", "Tukda", "Chakkardar", "Sam-se-sam"]


def select_composition_type(index: int):
    st.session_state.composition_type = index


st.selectbox(
    "Composition type",
    key="composition_type",
    options=COMPOSITION_TYPES,
)

st.text_area("Description", key="description")

st.button(
    "Generate Composition",
    on_click=lambda: generate(),
)

st.write(st.session_state.composition)
