# FastAPI Auth Service with JWT + PostgreSQL

## Запуск проекта

1. Установите [Docker Desktop](https://www.docker.com/products/docker-desktop/) или Docker + Docker Compose.
2. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/kevinclapton/auth-service.git
3. Подготовьте проект к запуску:
   cd auth-service
   cp .env.example .env
4. Измените данные POSTGRES_PASSWORD и SECRET_KEY в .env по своему усмотрению. Не забудьте также изменить паттерн your_postgres_password внутри DATABASE_URL.
5. Запустите готовый к работе проект:
   docker-compose up --build # Если необходимо наблюдать за работой контейнеров в реальном времени, либо
   docker-compose up -d --build # Если требуется запустить контейнеры в фоне и освободить терминал для работы
   