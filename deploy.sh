#!bin/bash

function deploy
{
    local project_id=$(gcloud config get-value project)
    local container_name="project-container"
    gcloud builds submit --tag gcr.io/"$project_id"/"$container_name"
    gcloud run deploy --image gcr.io/"$project_id"/"$container_name" --platform managed
}

deploy