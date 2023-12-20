# Dockerfile

# ベースイメージの指定
FROM python:3.8

# 作業ディレクトリの設定
WORKDIR /var/www/app

# パッケージのインストール
RUN apt-get update && \
    apt-get install -y apache2 openssl && \
    apt-get install -y

RUN sed -i 's!/var/www/html!/var/www/app!g' /etc/apache2/sites-available/000-default.conf

# ApacheのSSLモジュールを有効にする
ENV DEBIAN_FRONTEND=noninteractive
RUN a2enmod ssl && \
    a2enmod proxy && \
    a2enmod proxy_http
#ファイルを有効にする
RUN echo "ServerName localhost\n AddDefaultCharset UTF-8" | tee /etc/apache2/conf-available/fqdn.conf
RUN a2enconf fqdn


# webサイトのコンテンツコピー
COPY ./templates /var/www/app/templates
COPY ./static/js /var/www/app/static/js

# SSL証明書を配置するディレクトリを作成
RUN mkdir /etc/apache2/ssl

# SSL証明書と秘密鍵をコピー
COPY server.crt /etc/apache2/ssl
COPY server.key /etc/apache2/ssl

# Apacheの設定ファイルをコピー
COPY apache-ssl.conf /etc/apache2/sites-available/default-ssl.conf

# サイトを有効にする
RUN a2ensite default-ssl

# Pythonアプリのコピー
COPY ./ap.py /var/www/app/
COPY ./requirements.txt /var/www/app/

# Pythonライブラリのインストール
RUN pip install --no-cache-dir -r /var/www/app/requirements.txt

# ポートの開放
EXPOSE 443

# Apacheを起動
#CMD ["apache2ctl", "-D", "FOREGROUND"]
CMD ["gunicorn", "-b", "0.0.0.0:443", "--keyfile", "/etc/apache2/ssl/server.key", "--certfile", "/etc/apache2/ssl/server.crt", "ap:app"]
