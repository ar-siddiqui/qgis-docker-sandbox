FROM debian:buster-slim

ENV LANG=en_EN.UTF-8
ENV QT_QPA_PLATFORM="offscreen"

RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests --allow-unauthenticated -y \
    gnupg \
    ca-certificates \
    wget \
    locales \
    && localedef -i en_US -f UTF-8 en_US.UTF-8 \
    # Add the current key for package downloading - As the key changes every year at least
    # Please refer to QGIS install documentation and replace it and its fingerprint value with the latest ones
    && wget -O - https://qgis.org/downloads/qgis-2021.gpg.key | gpg --import \
    && gpg --export --armor 46B5721DBBD2996A | apt-key add - \
    && echo "deb http://qgis.org/debian buster main" >> /etc/apt/sources.list.d/qgis.list \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests --allow-unauthenticated -y \
    qgis \
    qgis-plugin-grass \
    && apt-get remove --purge -y \
    gnupg \
    wget \
    && rm -rf /var/lib/apt/lists/*  

RUN apt-get update \
    && apt-get -y install curl \
    && curl https://plugins.qgis.org/plugins/curve_number_generator/version/1.3/download/ --output curve_number_generator.zip \
    && apt-get install unzip \
    && unzip curve_number_generator.zip -d /usr/share/qgis/python/plugins \
    && rm curve_number_generator.zip \
    && qgis_process plugins enable curve_number_generator

COPY requirements.txt /

RUN apt-get -y install python3-pip && \
    pip3 install -r requirements.txt

WORKDIR /app

ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0", "-p", "5000" ]