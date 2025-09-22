FROM python:3.13-slim

WORKDIR /app

# Сначала ставим системные пакеты
RUN apt-get update && apt-get install -y wireguard-tools iproute2 && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install "poetry==2.0.1"
RUN pip install alembic


# Копируем только файлы зависимостей для кеширования
COPY pyproject.toml poetry.lock ./

# Ставим Python-зависимости
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем исходники
COPY . .

# Запуск
CMD ["poetry", "run", "python", "-m", "app.main"]
