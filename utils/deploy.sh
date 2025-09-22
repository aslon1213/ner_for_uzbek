
sudo docker build -t aslon1213/ner_for_names .
sudo docker stop ner_for_names && sudo docker rm ner_for_names
sudo docker run -d -p 5001:8000 --mount type=bind,source=/Users/aslonkhamidov/Desktop/code/consultant_ai/ner_for_names,target=/app/ --net consultant_ai --name ner_for_names aslon1213/ner_for_names
