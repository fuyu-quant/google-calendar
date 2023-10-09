FROM python:3.9.13-slim
USER root

# environment
ENV LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"
ENV TZ JST-9


COPY requirements.txt /root/

# Installing packages
WORKDIR /root
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /root/src/
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8060", "--server.address=0.0.0.0"]
