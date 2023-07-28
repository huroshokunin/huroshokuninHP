<<<<<<< HEAD
# PHPの公式イメージをベースにする
FROM php:latest

# 必要なPHPの拡張機能をインストールする
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Apacheの設定ファイルをコピーする
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

# mod_rewriteを有効にする
RUN a2enmod rewrite

# Apacheを再起動する
RUN service apache2 restart

# コンテナ内にアプリケーションをコピーする
COPY . /var/www/html

# コンテナ内の作業ディレクトリを設定する
WORKDIR /var/www/html

# コンテナが外部と通信する際のデフォルトのポートを設定する
EXPOSE 80

# Apacheをバックグラウンドで起動する
CMD ["apache2-foreground"]
=======
# Dockerfile
FROM php:7.4-apache

# Install git
RUN apt-get update && apt-get install -y git

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY . /var/www/html

EXPOSE 80
>>>>>>> 522650ce1c0425f2cfa9a872df1cecdb03296f1d
