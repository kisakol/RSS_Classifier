FROM python:3.9-slim

WORKDIR /app

# Copy the full repo into the image
COPY . .

# Install dependencies and the package itself
RUN pip install --no-cache-dir \
    numpy==1.21.0 \
    pandas==1.2.1 \
    scikit-learn==0.24.2 \
    xgboost==1.4.2 \
    && pip install --no-cache-dir -e .

ENTRYPOINT ["python"]
