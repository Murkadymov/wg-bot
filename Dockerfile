# ---- Stage 1: build dependencies ----
FROM python:3.13-slim AS builder

WORKDIR /app

# Устанавливаем Poetry
RUN pip install "poetry==1.8.3"

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Экспортируем зависимости в requirements.txt
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt


# ---- Stage 2: runtime ----
FROM python:3.13-slim

WORKDIR /app

# Копируем requirements.txt из builder-слоя
COPY --from=builder /app/requirements.txt .

# Ставим зависимости без Poetry
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники бота
COPY . .

# Запускаем бота
CMD ["python", "-m", "app.main"]
