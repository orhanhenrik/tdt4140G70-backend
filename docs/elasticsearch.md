# Installing elasticsearch
* [Install java](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04)
* [Install elastic](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-16-04#step-1-%E2%80%94-downloading-and-installing-elasticsearch)

## Install [ingest-plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/ingest-attachment.html)
* Run `/usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-attachment`

# Configure elasticsearch

## Inside `/etc/elasticsearch/jvm.options`
* Set `-Xms256m`
* Set `-Xmx1g`

## Inside `/etc/elasticsearch/elasticsearch.yml`
* Set `network.host: 127.0.0.1`, so that only our server can access elastic
