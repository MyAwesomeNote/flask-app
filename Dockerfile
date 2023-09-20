FROM python:3.11-slim-buster AS build-image

WORKDIR /app

COPY . /app

RUN apt-get update && \
  apt-get install -y --no-install-recommends libgl1-mesa-glx libglib2.0-0 \
  && pip install --no-cache-dir -r requirements.txt \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN rm -rf ./migrations && rm -f *.db *.sqlite && \
    python -m flask db init && \
    python -m flask db migrate && \
    python -m flask db upgrade && \
    chmod 666 *.db *.sqlite || true && \
    chmod 777 . || true && \
    python ./cmd/gen_model.py

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]