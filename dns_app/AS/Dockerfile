FROM python:3.9

WORKDIR /app
COPY . /app
RUN pip install Flask
RUN echo "Installation done"
EXPOSE 53533/udp
CMD [ "python", "./as.py" ]
