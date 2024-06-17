import streamlit as st
from project import user_proxy, manager
from composition_parser import get_composition_parser, Composition

COMPOSITION_TYPES = {
    "तिहाई": "Tihai",
    "टुकड़ा": "Tukda",
    "चक्करदार टुकड़ा": "Chakkardar",
    "सम-से-सम टुकड़ा": "Sam-se-sam",
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

sidebar, main = st.columns([1, 1])

sidebar.image(
    "https://media.canva.com/v2/image-resize/format:PNG/height:2400/quality:100/uri:s3%3A%2F%2Fmedia-private.canva.com%2FeepwA%2FMAGIZteepwA%2F1%2Fp.png/watermark:F/width:1582?csig=AAAAAAAAAAAAAAAAAAAAAA41I39rgY0rAJnAC5CRbGB5BCrHUxiZ94SbNFmflq4t&exp=1718662812&osig=AAAAAAAAAAAAAAAAAAAAAF4DTY66za7iraI2xMlWyl6r1GA66J5tzgH0Vr6Dq393&signer=media-rpc&x-canva-quality=screen_3x",
    width=200,
)
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
