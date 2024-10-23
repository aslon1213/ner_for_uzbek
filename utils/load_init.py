import spacy
from deeppavlov import build_model
import os

# load model
print("1. Loading Models...")
# print("MODE: ", os.getenv("MODE"))
if os.getenv("MODE") is not None:
    print("Loading remote model")
    ner_model_uz = build_model("utils/ner_onnotes_bert.json", download=False)
else:
    print("Loading local model")
    ner_model_uz = build_model("utils/ner_onnotes_bert_local.json", download=False)
print("2. Model for UZ loaded")
ner_model_ru = spacy.load("ru_core_news_sm")
print("3. Model for RU loaded")
