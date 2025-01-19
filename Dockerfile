# Use the official Python slim image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port (optional; for debugging or future use)
EXPOSE 8080

# Set the environment variable for the bot token
#ENV TELEGRAM_BOT_TOKEN=""

# Run the bot
CMD ["python", "bubblo2.py"]

#docker run -d --name telegram-bot -e TELEGRAM_BOT_TOKEN=7594608816:AAHmbPAvsAYieuJ1nEAHqungwNL03kPjDSk
#aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 515966516798.dkr.ecr.ap-southeast-2.amazonaws.com
#C:\Program Files\Amazon\AWSCLIV2\
#docker tag telegram-bot:latest 515966516798.dkr.ecr.ap-southeast-2.amazonaws.com/telebot:latest
#docker push 515966516798.dkr.ecr.ap-southeast-2.amazonaws.com/telebot:latest
