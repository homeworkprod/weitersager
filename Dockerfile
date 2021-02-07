FROM python:3.9-slim

RUN pip install weitersager==0.5

COPY ./config.toml .

EXPOSE 8080

CMD ["weitersager", "config.toml"]
