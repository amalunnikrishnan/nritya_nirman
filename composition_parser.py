import json
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_groq import ChatGroq


class Composition(BaseModel):
    """
    A Kathak composition which can be defined as a collection of bols.
    Groups of bols are segments. Each segment is separated by a newline (\n).
    A segment is a list of bols.
    Bols are separated by pipes (|). Each bol is a string.
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
        return "\n\n".join([" | ".join(segment) for segment in self.segments])

    def __str__(self) -> str:
        return self.stitched()


def get_composition_parser():
    config = json.load(open("./GROQ_CONFIG_LIST.json"))[0]
    model = ChatGroq(api_key=config["api_key"], model=config["model"])
    return model.with_structured_output(Composition)
