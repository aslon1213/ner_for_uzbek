from fastapi import FastAPI
from deeppavlov import build_model, configs
from pydantic import BaseModel
import spacy
from typing import List

app = FastAPI()


# load model
print("1. Loading Models...")
ner_model_uz = build_model("ner_onnotes_bert.json", download=False)
print("2. Model for UZ loaded")
ner_model_ru = spacy.load("ru_core_news_sm")
print("3. Model for RU loaded")


class NerInput(BaseModel):
    texts: List[str]


@app.get("/")
async def predict_ner(NerInput: NerInput):
    output = {}
    res_uz = ner_model_uz(NerInput.texts)
    output["uz"] = res_uz
    for text in NerInput.texts:
        doc = ner_model_ru(text)
        res_ru = [(ent.text, ent.label_) for ent in doc.ents]
        output["ru"] = res_ru
    return output
