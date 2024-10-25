from typing import List
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import spacy
from deeppavlov import build_model
from fastapi import FastAPI, Response
from pydantic import BaseModel
import os

app = FastAPI()
# Prometheus a Counter metric
REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")


# load model
print("1. Loading Models...")
# print("MODE: ", os.getenv("MODE"))
# if os.getenv("MODE") is not None:
#     print("Loading remote model")
#     ner_model_uz = build_model("ner_onnotes_bert.json", download=False)
# else:
print("Loading local model")
ner_model_uz = build_model("./utils/ner_onnotes_bert_local.json", download=False)
print("2. Model for UZ loaded")
ner_model_ru = spacy.load("ru_core_news_sm")
print("3. Model for RU loaded")


class NerInput(BaseModel):
    texts: List[str]


words = ["muddatli", "smartbank", "pul"]
word_replacements = {
    "akamga": "aka",
    "akam": "aka",
    "akamni": "aka",
    "akamning": "aka",
    "akajon": "aka",
    "akasi": "aka",
    "akasini": "aka",
    "akasining": "aka",
    "togam": "toga",
    "togani": "toga",
    "toganing": "toga",
    "togasini": "toga",
    "togasining": "toga",
    "dadam": "dada",
    "dadamni": "dada",
    "dadamga": "dada",
    "dadamning": "dada",
    "otam": "ota",
    "otamni": "ota",
    "otamga": "ota",
    "otamning": "ota",
    "onam": "ona",
    "onamni": "ona",
    "onamga": "ona",
    "onamning": "ona",
    "amakim": "amaki",
    "amakimni": "amaki",
    "amakimga": "amaki",
    "amakimning": "amaki",
}


@app.get("/many")
async def predict_ner(NerInput: NerInput):
    REQUEST_COUNT.inc()
    texts = NerInput.texts
    output = {"uz": {}, "ru": {}}
    # for text in texts:
    #     for word in word_replacements:
    #         text = text.replace(word, word_replacements[word])
    res_uz = ner_model_uz(texts)
    # if muddatli is
    for i, t in enumerate(res_uz[0][0]):
        if any([word in t.lower() for word in words]):
            res_uz[1][0][i] = "O"
        if t.lower() == "muddatli":
            res_uz[1][0][i] = "O"
        if t.lower() == "smartbank":
            res_uz[1][0][i] = "O"
        if t.lower() == "pul":
            res_uz[1][0][i] = "O"
        if t.lower() in word_replacements:
            res_uz[1][0][i] = "B-PERSON"

    # replaace the word from akamni to aka, etc
    print(res_uz[0])
    for i in range(len(res_uz[0])):
        for j in range(len(res_uz[0][i])):
            word = res_uz[0][i][j]
            if word.lower() in word_replacements:
                res_uz[0][i][j] = word_replacements[word.lower()]

    output["uz"]["texts"] = res_uz[0]
    output["uz"]["entities"] = res_uz[1]
    for text in texts:
        doc = ner_model_ru(text)
        res_ru = [(ent.text, ent.label_) for ent in doc.ents]

        # leave only entities which are person or per
        output["ru"]["texts"] = [text.split()]
        output["ru"]["entities"] = res_ru
    # print in red

    print(f"\033[91m {output}\033[00m")
    return output


@app.get("/")
async def predict_ner_single(text: str):
    REQUEST_COUNT.inc()
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
    print(f"\033[91m {output}\033[00m")
    return output


@app.get("/metrics")
def metrics():
    # Generate latest metrics for Prometheus
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
