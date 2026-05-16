FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Dependencias necesarias para Playwright + Chromium + ffmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    wget \
    ca-certificates \
    libnspr4 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    fonts-liberation \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Instalar Chromium para Playwright
RUN python -m playwright install chromium

# Copiar proyecto
COPY . .

# Crear carpetas necesarias
RUN mkdir -p /downloads /cookies

CMD ["python", "app.py"]
