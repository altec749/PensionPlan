FROM node:24.0.0-alpine AS ui-build

WORKDIR /ui
COPY ui/ ./

# COPY ui/package.json ui/package-lock.json ./
RUN npm ci
RUN npm run build


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py pension.py ./
COPY --from=ui-build /ui/dist/ui/browser /app/static

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
