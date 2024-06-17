import json
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_groq import ChatGroq


def get_model():
    config = json.load(open("./GROQ_CONFIG_LIST.json"))[0]
    model = ChatGroq(api_key=config["api_key"], model=config["model"])
    return model


SEGMENT_SEP = "\n\n"
BOL_SEP = " | "

MAPPING = {
    "a": "अ",
    "aa": "आ",
    "da": "दा",
    "dha": "धा",
    "dhi": "धि",
    "dhin": "धिन",
    "di": "दि",
    "dig": "दिग",
    "ga": "गा",
    "ge": "गे",
    "ghi": "घि",
    "hta": "हता",
    "ka": "का",
    "kat": "कत",
    "kdan": "कदन",
    "ki": "कि",
    "na": "ना",
    "nga": "ंगा",
    "ra": "रा",
    "ta": "ता",
    "tat": "तत्",
    "tha": "था",
    "thei": "थई",
    "thu": "थु",
    "thun": "थुन",
    "ti": "ति",
    "tig": "तिग",
    "tram": "त्रम",
    "tta": "त्ता",
}


class Composition(BaseModel):
    """
    A Kathak composition which can be defined as a collection of bols.
    Groups of bols are segments. Each segment is separated by a newline (\n).
    If there are no newlines (\n), treat the entire composition as a single
    segment.
    A segment is a list of bols.
    Bols are separated by pipes (|). Each bol is a string.
    Each bol consists of words that are separated by spaces.
    A bol usually contains multiple words.
    """

    segments: List[List[str]] = Field(
        description="A list of list of bols in a Kathak composition."
    )

    @validator("segments", allow_reuse=True)
    @classmethod
    def validate_bols(cls, segments: List[List[str]]):
        out: List[List[str]] = []
        for segment in segments:
            new_segment = [bol for bol in [bol.strip() for bol in segment] if bol]
            if new_segment:
                out.append(new_segment)
        return out

    def count_beats(self):
        """Counts the number of beats in a composition"""
        return len([bol for segment in self.segments for bol in segment])

    def is_valid(self) -> bool:
        return self.count_beats() > 0

    def vocab(self):
        return set(
            [
                [
                    word
                    for segment in self.segments
                    for bol in segment
                    for word in bol.split()
                ]
            ]
        )

    def stitched(self):
        return SEGMENT_SEP.join([BOL_SEP.join(segment) for segment in self.segments])

    def __str__(self) -> str:
        return self.stitched()

    @staticmethod
    def _transliterate_bol(bol: str):
        return " ".join([MAPPING.get(word, word) for word in bol.split() if word])

    def transliterated(self) -> "Composition":
        return self.__class__(
            segments=[
                [self.__class__._transliterate_bol(bol) for bol in segment]
                for segment in self.segments
            ]
        )


def get_composition_parser():
    model = get_model()
    return model.with_structured_output(Composition)
