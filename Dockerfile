# Берём слим питон 3.14 как в проекте
FROM python:3.14-slim

# Смена директории на /app
WORKDIR /app

# Копируем requirements в /app
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Дефолтная команда для запуска тестов
CMD ["pytest", "-v"]