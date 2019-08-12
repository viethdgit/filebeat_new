 #!/bin/sh
 
 cat > /etc/filebeat/filebeat.yml <<END
filebeat:
  prospectors:
  -
    paths:
      - /usr/local/webclip/logs/clip.vn-access.log
    input_type: log
    fields:
      type: weblog
      host_name: ${HOSTNAME}
      group_name: web.clip
    fields_under_root: true
  spool_size: 4096
output:
  elasticsearch:
    hosts: ["172.18.10.106:9208","172.18.10.106:9209", "172.18.10.107:9208","172.18.10.107:9209", "172.18.10.108:9208","172.18.10.108:9209","172.25.0.15:9208","172.25.0.15:9209","172.25.0.16:9208","172.25.0.16:9209", "172.25.0.14:9208","172.25.0.14:9209"]
    worker: 4
    bulk_max_size: 2048
    index: "weblog-%{[host_name]}-%{+YYYY.MM.dd}"
    template.enabled: true
    template.path: "filebeat.template.json"
    template.overwrite: false
logging:
  level: error
END
