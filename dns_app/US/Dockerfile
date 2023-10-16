FROM python:3.9

WORKDIR /app
COPY . /app
RUN pip install Flask
RUN echo "Installation done"
EXPOSE 8080
CMD [ "python", "./us.py" ]
