wget https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-6.2.0-linux-x86_64.tar.gz
tar -xvzf filebeat-6.2.0-linux-x86_64.tar.gz
rm -rf filebeat-6.2.0-linux-x86_64.tar.gz
mv filebeat-6.2.0-linux-x86_64 /opt/filebeat2
echo "#"> /opt/filebeat2/filebeat.yml

cat > /etc/systemd/system/filebeat2.service <<END
[Unit]
Description=filebeat
Documentation=https://www.elastic.co/guide/en/beats/filebeat/current/index.html
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/opt/filebeat2/filebeat -c /opt/filebeat2/filebeat.yml -path.home /opt/filebeat2/ -path.config /opt/filebeat2/ -path.data /var/lib/filebeat -path.logs /var/log/filebeat
Restart=always

[Install]
WantedBy=multi-user.target
END