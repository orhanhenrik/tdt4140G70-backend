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

## Development
Use the following [DockerFile](https://gist.github.com/jfremstad/320ea3e3a0929faabb40260807bc854c) and run `docker build -t elastic-ingest:5.2.2 .` to build it.

Run `docker run -p 9200:9200 -e "http.host=0.0.0.0" -e "transport.host=127.0.0.1" elastic-ingest:5.2.2` to start the elasticsearch server.

Username: elasticsearch

Password: changeme

# Using elasticsearch
## Upload PDF
Run `./fileToJSON.sh My_PDF_File.pdf` followed by
`curl "http://elastic:changeme@127.0.0.1:9200/my_index/my_type/<<SOME_NUMBER>>?pipeline=attachment" -d @My_PDF_File.pdf.json`
