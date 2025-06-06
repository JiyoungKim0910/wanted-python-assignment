#!/bin/bash

echo "Waiting for DB to be ready..."

echo "Loading sample data..."
python load_sample_data.py

echo "Done!"

echo "Running pytest.."
pytest test_senior_app.py

echo "FastAPI 서버 시작!"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
