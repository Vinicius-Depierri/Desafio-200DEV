# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o contêiner
COPY . /app/

# Exponha a porta que a aplicação vai rodar
EXPOSE 8081

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
