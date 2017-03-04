# Installing elasticsearch
* [Install java](https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04)
* [Install elastic](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-16-04#step-1-%E2%80%94-downloading-and-installing-elasticsearch)

## Install [ingest-plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/current/ingest-attachment.html)
* Run `/usr/share/elasticsearch/bin/elasticsearch-plugin install ingest-attachment`

## Install [Kibana](https://www.elastic.co/guide/en/kibana/current/deb.html)
A web interface for creating and sending queries.
After installation you can find it at [http://127.0.0.1:5601](http://127.0.0.1:5601)

# Configure elasticsearch

## Inside `/etc/elasticsearch/jvm.options`
* Set `-Xms256m`
* Set `-Xmx1g`

## Inside `/etc/elasticsearch/elasticsearch.yml`
* Set `network.host: 127.0.0.1`, so that only our server can access elastic

## Development
Use the following Dockerfile and run `docker build -t elastic-ingest:5.2.2 .` to build it.
```
FROM docker.elastic.co/elasticsearch/elasticsearch:5.2.2
RUN bin/elasticsearch-plugin install ingest-attachment
```
Run `docker run -p 9200:9200 -e "http.host=0.0.0.0" -e "transport.host=127.0.0.1" elastic-ingest:5.2.2` to start the elasticsearch server.
