# Dockerfile para appWeb/user (Next.js + Node.js)
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de dependencias
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de la aplicación
COPY . .

# Construye la aplicación Next.js
RUN npm run build

# Expone el puerto por defecto de Next.js
EXPOSE 3000

# Comando por defecto para iniciar la app
CMD ["npm", "start"]
