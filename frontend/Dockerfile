FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application source code
COPY . .

# Build Next.js production build
RUN npm run build

# Expose Next.js port
EXPOSE 3000

# Start production server
CMD ["npm", "start"]
