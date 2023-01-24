FROM python:3.10
WORKDIR /PdrBot
COPY requirements.txt /PdrBot/
RUN pip install -r requirements.txt
COPY . /PdrBot
WORKDIR /PdrBot/VkBot/db
RUN alembic upgrade head
WORKDIR /PdrBot/VkBot
CMD python bot.py


