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


@app.get("/many")
async def predict_ner(NerInput: NerInput):
    texts = NerInput.texts
    output = {"uz": {}, "ru": {}}
    res_uz = ner_model_uz(texts)
    output["uz"]["texts"] = res_uz[0]
    output["uz"]["entities"] = res_uz[1]
    for text in texts:
        doc = ner_model_ru(text)
        res_ru = [(ent.text, ent.label_) for ent in doc.ents]

        # leave only entities which are person or per
        output["ru"]["texts"] = [text.split()]
        output["ru"]["entities"] = res_ru
    return output


@app.get("/")
async def predict_ner_single(text: str):
    output = {"uz": {}, "ru": {}}

    texts = [text.strip()]
    res_uz = ner_model_uz(texts)
    output["uz"]["texts"] = res_uz[0]
    output["uz"]["entities"] = res_uz[1]
    for text in texts:
        doc = ner_model_ru(text)
        res_ru = [(ent.text, ent.label_) for ent in doc.ents]

        # leave only entities which are person or per
        output["ru"]["texts"] = [text.split()]
        output["ru"]["entities"] = res_ru
    return output