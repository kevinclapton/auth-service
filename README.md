# FastAPI Auth Service with JWT + PostgreSQL

---

## Требования

Перед запуском убедитесь, что у вас установлено:

- **Docker** и **Docker Compose**  
  [Скачать Docker Desktop (включает оба)](https://www.docker.com/products/docker-desktop/)
- **Git** (для клонирования репозитория)  
  [Скачать Git](https://git-scm.com/)
- **64-битная ОС** (Windows, Linux или macOS)
- **Минимум 2 ГБ свободного места на диске** (Docker-образы и контейнеры)

> Docker Desktop включает всё необходимое.

## Запуск проекта


### 1. Клонируйте репозиторий
   ```bash
   git clone https://github.com/kevinclapton/auth-service.git
   cd auth-service
   ```
### 2. Подготовьте файл окружения
   ```bash
   cp .env.example .env
   ```
### 3. Настройте переменные (опционально)
Откройте .env и при необходимости измените:
- POSTGRES_PASSWORD — пароль для PostgreSQL;
- SECRET_KEY — секретный ключ для JWT (должен быть длинным и случайным).
- Убедитесь, что DATABASE_URL использует тот же пароль:
>DATABASE_URL=postgresql+psycopg2://postgres:ВАШ_ПАРОЛЬ@db:5432/fastapi_auth

## Проверка работы

После запуска сервис предоставляет интерактивную документацию и API для тестирования.
### 1. Запустите контейнеры
   ```bash
   docker-compose up --build
   ```
   >Если необходимо наблюдать за работой контейнеров в реальном времени
   
   либо
   ```bash
   docker-compose up -d --build
   ```
   >Если требуется запустить контейнеры в фоне и освободить терминал для работы

Сервис станет доступен:
- API: http://127.0.0.1:8000
- Документация: http://127.0.0.1:8000/docs
### 2. Протестируйте API
Сначала зарегистрируйте пользователя. Для этого:
- Перейдите на http://127.0.0.1:8000/docs
- Найдите POST /register
- Нажмите "Try it out"
- Введите:
   ```json
   {
      "username": "testuser",
      "password": "securepassword123"
   }
   ```
- Нажмите Execute. Ожидаемый ответ:
   ```json
   {
      "message": "Пользователь успешно зарегистрирован",
      "username": "testuser"
   }
   ```
Проверьте авторизацию созданного пользователя. Для этого:
- Найдите POST /auth
- Введите в поле username:
>testuser

   в поле password:
>securepassword123
- Нажмите Execute. Ожидаемый ответ:
   ```json
   {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxx",
      "token_type": "bearer"
   }
   ```
- Нажмите кнопу Authorize в правом верхнем углу страницы
- В открывшемся окне введите в поле username:
>testuser

   в поле password:
>securepassword123
- Нажмите кнопку Authorize. В окне высветится сообщение о произошедшей авторизации. Можете закрыть окно, нажав на кнопку Close

Проверьте доступ к профилю. Для этого:
- Найдите GET /profile
- Нажмите Try it out, затем Execute
   Ожидаемый ответ:
   ```json
   {
      "username": "testuser"
   }
   ```
Вывод данного сообщения одначает, что токен JWT, сгенерированный при совершении авторизации, распознан, что пользователь аутентифицирован, а также маршрут защищён.

## Структура проекта

```text
auth-service/
├── .env.example          # Шаблон переменных окружения
├── docker-compose.yml    # Запуск FastAPI + PostgreSQL
├── Dockerfile            # Сборка FastAPI-образа
├── requirements.txt      # Зависимости Python
└── app/
   ├── __init__.py
   ├── main.py            # Основное FastAPI-приложение
   ├── database.py        # Модель пользователя и подключение к БД
   └── wait_for_db.py     # Скрипт ожидания готовности PostgreSQL (без него контейнеры Docker взаимодействуют некорректно)
```

## Перезапуск с чистой БД

Если нужно сбросить всё:
   ```bash
   docker-compose down
   docker volume rm auth-service_postgres_data
   docker-compose up --build
   ```