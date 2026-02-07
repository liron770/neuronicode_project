FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# התקנת ספריות מערכת (בשביל OpenCV ו-FFmpeg)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# שדרוג כלי התקנה
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# התקנת כל הדרישות מקובץ אחד
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת שאר הפרויקט
COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "receiver.py"]