
FROM node:20-slim as builder

WORKDIR /app

# Copy frontend
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install

COPY frontend ./frontend/
RUN cd frontend && npm run build

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt --break-system-packages

# Copy backend code
COPY backend ./backend/

# Copy built frontend
COPY --from=builder /app/frontend/dist ./backend/frontend_dist/

EXPOSE 8000

CMD cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000

