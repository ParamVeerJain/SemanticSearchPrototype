FROM python:3.9-slim 
#yeh upar ke line ka use karte hue hum python 3.9 ka image use kar rahe hain
WORKDIR /app
#yeh dono ka ka matlab hai , ki hum apne current directory ke saare files ko /app directory mein copy kar rahe hain , first ka matlab hai ki hum requirements.txt file ko copy kar rahe hain aur second ka matlab hai ki hum saare files ko copy kar rahe hain
EXPOSE 8501
#/app ka matlab hai ki humara work directory /app hoga , jahan pe hum apna code run karenge
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libsqlite3-dev \
    libsodium-dev \
    libz-dev \
    libcurl4-openssl-dev \
    libprotobuf-dev \
    protobuf-compiler \
    xz-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    # isme last mein rm use karke hum , apt-get update ke cache ko clean kar rahe hain 

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
#yeh upar ke line ka use karke hum requirements.txt file ko install kar rahe hain aur extra cache ko clean kar rahe hain

COPY . .

CMD ["streamlit", "run", "./search.py"]