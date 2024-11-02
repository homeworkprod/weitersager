FROM python:3.11-slim

WORKDIR /app

# Don't run as root.
RUN useradd --create-home user
USER user
ENV PATH /home/user/.local/bin:$PATH

RUN pip install --no-cache-dir weitersager==0.12.0-dev

EXPOSE 8080

CMD ["weitersager", "config.toml"]
