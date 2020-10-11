FROM python:3.8

RUN pip install weitersager==0.4

COPY ./config.toml .

EXPOSE 8080

CMD ["weitersager", "config.toml"]
