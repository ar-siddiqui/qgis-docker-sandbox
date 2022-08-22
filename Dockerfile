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
    && wget -O - https://qgis.org/downloads/qgis-2022.gpg.key | gpg --import \
    && gpg --export --armor D155B8E6A419C5BE | apt-key add - \
    && echo "deb http://qgis.org/debian buster main" >> /etc/apt/sources.list.d/qgis.list \
    && apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests --allow-unauthenticated -y \
    qgis \
    && apt-get remove --purge -y \
    gnupg \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get -y install curl \
    && apt-get install unzip

COPY requirements.txt /
COPY plugins.txt /
COPY install_plugins.sh /

RUN bash install_plugins.sh

RUN apt-get -y install python3-pip && \
    pip3 install -r requirements.txt

WORKDIR /app

ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0", "-p", "5000" ]