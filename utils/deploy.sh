
sudo docker build -t aslon1213/ner_for_names .
sudo docker stop ner_for_names && sudo docker rm ner_for_names
sudo docker run -d -p 5001:8000 --net consultant_ai --name ner_for_names aslon1213/ner_for_names
