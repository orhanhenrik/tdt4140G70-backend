#!/bin/bash

# Start elasticsearch
systemctl start elasticsearch.service

# Wait 10 seconds
sleep 10

# Initialize ingest-plugin
curl -X PUT 'http://127.0.0.1:9200/_ingest/pipeline/attachment' -d @initialize_elastic.json

cd tdt4140G70-backend
source venv/bin/activate
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver 0.0.0.0:8000
