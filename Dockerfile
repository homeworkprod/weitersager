FROM python:3.9-slim

# Don't run as root.
RUN useradd --create-home user
USER user
WORKDIR /home/user
ENV PATH /home/user/.local/bin:$PATH

RUN pip install weitersager==0.7

COPY ./config.toml .

EXPOSE 8080

CMD ["weitersager", "config.toml"]
