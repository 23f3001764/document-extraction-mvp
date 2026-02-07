#!/bin/bash

echo "🚀 Starting Document Extraction MVP deployment..."

docker compose down
docker compose build
docker compose up -d

echo "✅ Application deployed successfully"
echo "🌐 Access the app on port 8501"