
sudo docker build -t aslon1213/ner_for_names .
sudo docker stop ner_for_names && sudo docker rm ner_for_names
sudo docker run -d  --mount type=bind,source=/home/aslonhamidov/work/ner_for_uzbek/ner_for_uzbek/person_ner_server.py,target=/app/person_ner_server.py  --mount type=bind,source=/home/aslonhamidov/work/ner_for_uzbek/ner_for_uzbek/utils,target=/app/utils  -p 5001:8000 --net consultant_ai --name ner_for_names aslon1213/ner_for_names
