# Используем официальный образ Node.js
FROM node:22

# Создаем директорию для приложения
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json package-lock.json ./
RUN npm install

# Копируем остальные файлы
COPY . .

# Указываем порт
EXPOSE 4000

# Запускаем сервер
CMD ["node", "server.js"]