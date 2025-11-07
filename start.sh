FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY . .
RUN pip install frappe-bench && pip install -r requirements.txt

# Expose port
EXPOSE 8000

CMD ["bench", "start"]
