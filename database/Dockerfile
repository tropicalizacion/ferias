FROM postgres:18.3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-18-postgis-3 \
    postgresql-18-postgis-3-scripts \
    && rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /usr/local/bin/custom-database-entrypoint.sh

RUN chmod +x /usr/local/bin/custom-database-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/custom-database-entrypoint.sh"]
CMD ["postgres"]