FROM bitnami/postgresql:15

LABEL name "postgres_master_db_for_replication_cluster"
LABEL maitainer_mail arrian8@yandex.ruF
VOLUME /bitnami/postgresql
ENV POSTGRESQL_REPLICATION_MODE=master
ENV REPLICATION_USER=repluser
ENV REPLICATION_PASSWORD=12345 

ENV POSTGRESQL_DATABASE=master_db
ENV POSTGRESQL_USER=user
ENV POSTGRESQL_PASSWORD=qwerty
ENV ALLOW_EMPTY_PASSWORD=yes
