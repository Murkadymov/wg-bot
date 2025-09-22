FROM python:3.13-slim

WORKDIR /app

RUN pip install "poetry==2.0.1"

COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry install --no-root --no-interaction --no-ansi

# Копируем исходники
COPY . .

CMD ["poetry", "run", "python", "-m", "app.main"]