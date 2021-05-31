FROM mariadb:10.2

RUN apt-get update
RUN apt-get -y install locales-all

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

COPY mysql_charset2.cnf /etc/mysql/conf.d/mysqld_charset.cnf
