docker build -t aslon1213/ner_for_names .
docker stop ner_for_names && docker rm ner_for_names
docker run -d -p 5001:8000 --name ner_for_names aslon1213/ner_for_names