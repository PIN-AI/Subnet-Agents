FROM python:3.11-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    make \
    build-essential \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


RUN git clone https://github.com/PIN-AI/subnet-sdk.git


RUN pip install --no-cache-dir grpcio grpcio-tools protobuf
RUN cd subnet-sdk/python && make proto && pip install -e .


COPY . .


RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "agent3_reg.py"]
