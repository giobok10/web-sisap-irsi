FROM python:3.11

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    && apt-get clean

# Instalar el controlador ODBC para SQL Server
RUN curl https://download.microsoft.com/download/e/4/e/e4e67866-dffd-42d8-b076-415e083535b9/msodbcsql18_18.3.2.1-1_amd64.deb -o msodbcsql18.deb && \
    dpkg -i msodbcsql18.deb && \
    rm msodbcsql18.deb

# Configurar la aplicación
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "run:app"]
