import os

HOSTNAME=os.popen('hostname').read().strip().replace('.novalocal','').replace('vdc-','vdc1-').replace('fpt-','fpt1-')
GROUPNAME=HOSTNAME.split('-')[0] if HOSTNAME.split('-')[0] != 'bd' else 'vt2'

filebeat=''
yml_filebeat=['filebeat.prospectors:']
with open('/etc/filebeat/filebeat.yml') as f:
	filebeat= f.read()

live=False
vod=False
both=False
netstat_out=os.popen('netstat -tulnp').read()
if 'live' in HOSTNAME and '0.0.0.0:443' not in netstat_out:
	both=True
elif 'varnishd' not in netstat_out:
	vod=True
else:
	live=True

def varnishncsa():
	yml_filebeat.append('- type: log')
	yml_filebeat.append('  enabled: true')
	yml_filebeat.append('  json.keys_under_root: true')
	yml_filebeat.append('  json.add_error_key: true')
	yml_filebeat.append('  json.overwrite_keys: true')
	yml_filebeat.append('  paths:')
	yml_filebeat.append('    - /var/log/varnish/varnishncsa.log')
	yml_filebeat.append('    - /var/log/varnish/varnishncsa.log-20190815')
	yml_filebeat.append('  fields:')
	yml_filebeat.append('    type: "cdnlog_live"')
	yml_filebeat.append('    host_name: "%s"'%HOSTNAME.replace('vod','live'))
	yml_filebeat.append('    group_name: %s'%GROUPNAME)
	yml_filebeat.append('    index_prefix: "cdnlog-live"')
	yml_filebeat.append('  fields_under_root: true')
def nginx_access():
	yml_filebeat.append('- type: log')
	yml_filebeat.append('  enabled: true')
	yml_filebeat.append('  json.keys_under_root: true')
	yml_filebeat.append('  json.add_error_key: true')
	yml_filebeat.append('  json.overwrite_keys: true')
	yml_filebeat.append('  paths:')
	yml_filebeat.append('    - /usr/local/nginx-1.10.1/logs/access.log')
	yml_filebeat.append('    - /usr/local/nginx-1.10.1/logs/access.log-20190815')
	yml_filebeat.append('  fields:')
	yml_filebeat.append('    type: "cdnlog_vod"')
	yml_filebeat.append('    host_name: "%s"'%HOSTNAME.replace('live','vod').replace('vodd','vod') )
	yml_filebeat.append('    group_name: %s'%GROUPNAME)
	yml_filebeat.append('    index_prefix: "cdnlog-vod"')
	yml_filebeat.append('  fields_under_root: true')
def nginx_error():
	yml_filebeat.append('- type: log')
	yml_filebeat.append('  enabled: true')
	yml_filebeat.append('  paths:')
	yml_filebeat.append('    - /usr/local/nginx-1.10.1/logs/error.log')
	yml_filebeat.append('  fields:')
	yml_filebeat.append('    type: "nginx_error_log"')
	yml_filebeat.append('    host_name: "%s"'%HOSTNAME)
	yml_filebeat.append('    group_name: %s'%GROUPNAME)
	yml_filebeat.append('    index_prefix: "weblog-nginx-error"')
	yml_filebeat.append('  fields_under_root: true')
def trace_live():
	yml_filebeat.append('- type: log')
	yml_filebeat.append('  enabled: true')
	yml_filebeat.append('  json.keys_under_root: true')
	yml_filebeat.append('  json.add_error_key: true')
	yml_filebeat.append('  json.overwrite_keys: true')
	yml_filebeat.append('  paths:')
	yml_filebeat.append('    - /var/log/vcdn-live-agent-events.log')
	yml_filebeat.append('  fields:')
	yml_filebeat.append('    type: "cdnlog_trace_live"')
	yml_filebeat.append('    host_name: "%s"'%(HOSTNAME).replace('vod','live'))
	yml_filebeat.append('    group_name: %s'%GROUPNAME)
	yml_filebeat.append('    index_prefix: "cdnlog-trace"')
	yml_filebeat.append('  fields_under_root: true')
def trace_vod():
	yml_filebeat.append('- type: log')
	yml_filebeat.append('  enabled: true')
	yml_filebeat.append('  json.keys_under_root: true')
	yml_filebeat.append('  json.add_error_key: true')
	yml_filebeat.append('  json.overwrite_keys: true')
	yml_filebeat.append('  paths:')
	yml_filebeat.append('    - /var/log/vcdn-vod-agent-events.log')
	yml_filebeat.append('  fields:')
	yml_filebeat.append('    type: "cdnlog_trace_vod"')
	yml_filebeat.append('    host_name: "%s"'%(HOSTNAME).replace('live','vod'))
	yml_filebeat.append('    group_name: %s'%GROUPNAME)
	yml_filebeat.append('    index_prefix: "cdnlog-trace"')
	yml_filebeat.append('  fields_under_root: true')

if both == True:
	varnishncsa()
	nginx_access()
	nginx_error()
	trace_live()
	trace_vod()
elif live == True:
	varnishncsa()
	nginx_error()
	trace_live()
elif vod == True:
	nginx_access()
	nginx_error()
	trace_vod()
else:
	pass

if 'speedtest' in filebeat:
	yml_filebeat.append('- type: log')
	yml_filebeat.append('  enabled: true')
	yml_filebeat.append('  json.keys_under_root: true')
	yml_filebeat.append('  json.add_error_key: true')
	yml_filebeat.append('  json.overwrite_keys: true')
	yml_filebeat.append('  paths:')
	yml_filebeat.append('    - /var/www/html/speedtest/log.txt')
	yml_filebeat.append('  fields:')
	yml_filebeat.append('    type: "speedtest_log"')
	yml_filebeat.append('    host_name: "%s"'%(HOSTNAME))
	yml_filebeat.append('    group_name: %s'%GROUPNAME)
	yml_filebeat.append('    index_prefix: "speedtest"')
	yml_filebeat.append('  fields_under_root: true')


yml_filebeat.append('')
yml_filebeat.append('filebeat.config.modules:')
yml_filebeat.append('  path: ${path.config}/modules.d/*.yml')
yml_filebeat.append('  reload.enabled: false')
yml_filebeat.append('setup.template.name: "filebeat-dev"')
yml_filebeat.append('setup.template.pattern: "filebeat-dev-*"')
yml_filebeat.append('setup.template.fields: "fields.yml"')
yml_filebeat.append('setup.template.enabled: false')
yml_filebeat.append('setup.template.overwrite: false')
yml_filebeat.append('setup.template.settings:')
yml_filebeat.append('  index.number_of_shards: 3')
yml_filebeat.append('')
yml_filebeat.append('output.elasticsearch:')
yml_filebeat.append('  hosts: ["172.18.10.106:9208","172.18.10.106:9209", "172.18.10.107:9208","172.18.10.107:9209", "172.18.10.108:9208","172.18.10.108:9209", "172.25.0.15:9208","172.25.0.15:9209","172.25.0.16:9208","172.25.0.16:9209", "172.25.0.14:9208","172.25.0.14:9209"]')
yml_filebeat.append('  worker: 4')
yml_filebeat.append('  bulk_max_size: 2048')
yml_filebeat.append('  indices:')
yml_filebeat.append('   - index: "%{[index_prefix]}-%{[host_name]}-%{+YYYY.MM.dd}"')
yml_filebeat.append('')
yml_filebeat.append('logging.level: error')
yml_filebeat.append('logging.files:')
yml_filebeat.append('  path: /var/log/filebeat')
yml_filebeat.append('  name: filebeat2')
yml_filebeat.append('  keepfiles: 2')
yml_filebeat.append('filebeat.registry_file: 2-registry')


ker_ver=os.popen('uname -r').read()
path_yml='/opt/filebeat2/filebeat.yml'
if '2.' in ker_ver:
	path_yml='/etc/filebeat/filebeat.yml'
os.system('echo "#" > %s'%path_yml)

f = open (path_yml,'a')
for i in yml_filebeat:
	print i
	f.write(i+'\n')
f.close()
