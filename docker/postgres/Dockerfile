FROM postgres:17

# INSTALL REQUIRED PACKAGES
RUN apt update -y && apt upgrade -y \
    git \
    build-essential \
    postgresql-server-dev-17

# INSTALL PGVECTOR EXTENSION
RUN mkdir /tmp/pgvector
RUN cd /tmp/pgvector && git clone https://github.com/pgvector/pgvector.git
RUN cd /tmp/pgvector/pgvector && make && make install

# CLEAN UP
RUN apt-get remove -y git build-essential postgresql-server-dev-17 \
  && apt-get autoremove -y && apt-get clean

RUN rm -R /tmp/pgvector

# COPY INIT DB SCRIPT
COPY ./docker/postgres/init-db.sql /docker-entrypoint-initdb.d/init.sql
