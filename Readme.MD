# Product Card Finder

![Product Card Finder](https://i.ibb.co/tDsYmS7/2024-10-27-11-34-07.png)

## О проекте

Product Card Finder (http://150.241.66.50:5173/) — это приложение, которое позволяет пользователям искать карточки товаров по названию или категории. Приложение использует мощный стек технологий, включая React, Node.js, Express, MongoDB и Python для парсинга данных.

## Как это работает

1. **Поиск**: Клиент вводит название или категорию в поле ввода.
2. **Запрос на сервер**: Ввод отправляется на сервер.
3. **Парсинг данных**: На сервере Python-скрипты парсят данные с сайтов leroymerlin.ru и wildberries.ru и загружают их в базу данных MongoDB.
4. **Получение результатов**: Сервер обращается к базе данных и возвращает пользователю самые подходящие результаты.

## Технологии

- **Frontend**: React.js (vite)
- **Backend**: Node.js + Express
- **База данных**: MongoDB
- **Парсинг**: Python
- **Деплоймент**: VPS сервер с использованием Docker

## Установка

### Предварительные требования

- Docker
- Docker Compose

### Шаги установки

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/product-card-finder.git
   cd product-card-finder
   ```

2. Соберите и запустите приложение с помощью Docker:

   ```bash
   docker-compose up --build
   ```

3. Откройте приложение в браузере по адресу http://localhost:5173

## Структура проекта

```bash
/product-card-finder
├── /client              # Frontend на React
├── /server              # Backend на Node.js
├── /parser              # Python-скрипты для парсинга
├── Dockerfile.client    # Настройка докера для React
├── Dockerfile.server    # Настройка докера для Node.JS
├── Dockerfile.parsers   # Настройка докера для Python
└── docker-compose.yml   # Конфигурация Docker
```

## API

### Получение результатов поиска

- **URL**: /api/search
- **Метод**: POST
- **Тело запроса**:
  ```json
  {
    "query": "название или категория"
  }
  ```

## Пример ответа

```json
[
  {
    "product_title": "Название товара",
    "price": "Цена",
    "product_link": "Ссылка на товар",
    "images": ["photo.jpg", "photo1.jpg"],
    "product_description": "Описание"
  },
  ...
]
```

### P.S. пока парсинг адекватно работает только с leruamerlen, но уже есть почти готове решение для вайлдберрис и все масштабируемо
