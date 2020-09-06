#!/bin/bash

gcloud functions deploy survey --entry-point api_survey --runtime python37  --trigger-http --allow-unauthenticated --region asia-southeast2