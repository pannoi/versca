FROM python:3.11.3
WORKDIR /app
RUN apt-get update && \
	apt-get install -y gcc && \
	dpkg --add-architecture i386 && \
	apt clean && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && \
	pip install -r requirements.txt
COPY . .
CMD ["python", "-u", "main.py"]