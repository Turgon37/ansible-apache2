Ansible Role Apache2
========

[![Build Status](https://travis-ci.org/Turgon37/ansible-apache2.svg?branch=master)](https://travis-ci.org/Turgon37/ansible-apache2)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-Turgon37.apache2-blue.svg)](https://galaxy.ansible.com/Turgon37/apache2/)

## Description

:grey_exclamation: Before using this role, please know that all my Ansible roles are fully written and accustomed to my IT infrastructure. So, even if they are as generic as possible they will not necessarily fill your needs, I advice you to carrefully analyse what they do and evaluate their capability to be installed securely on your servers.

This roles configures an instance of Apache2 daemon.

## Requirements

Require Ansible >= 2.4

### Dependencies

If you use the zabbix monitoring profile you will need the role [ansible-zabbix-agent](https://github.com/Turgon37/ansible-zabbix-agent)

## OS Family

This role is available for Debian

## Features

At this day the role can be used to :

  * install Apache2
  * configure main server file
  * create virtualhosts configurations
  * manage enabled modules
  * override some modules configurations
  * monitoring items for
    * Zabbix
  * [local facts](#facts)

## Configuration

### Server

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in table below. To see default values please refer to this file.

| Name                          | Description                                                                                                      |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `apache2__version`            | Choose the apache2 version to install (as available in os repositories) Ex: 2.4.25-3+deb9u5                      |
| `apache2__service_enabled`    | A boolean that enable or not the apache service on boot and at runtime                                           |
| `apache2__service_restartable`| If true, the apache service will be automatically restarted on configuration changes (set to false in production)|
| `apache2__server_tokens`      | Configure the verbosity of the server token in error pages                                                       |
| `apache2__server_signature`   | Print or not the server signature on error pages                                                                 |
| `apache2__trace_enable`       | Configure the HTTP TRACE method                                                                                  |
| `apache2__ssl_ciphers`        | List the available SSL ciphers, by default only a recommanded subset is configured                               |
| `apache2__ssl_protocols`      | List the enabled SSL protocols, by default all except SSL 2/3                                                    |
| `apache2__ssl_honorciphers`   | Tell to server to prefer it's cipher order instead of client's one                                               |
| `apache2__log_formats`        | A dictionnary that contains all log formats available in apache.                                                 |
| `apache2__listen_http`        | List of port/host:port on which apache will listen for http requests                                             |
| `apache2__listen_https`       | List of port/host:port on which apache will listen for https requests                                            |

Note about apache2__listen_http(s), for now theses directives are filled manually, I planned to generate it automatically but it appear complicated because virtual hosts can be defined using include_role.

The following variable apply to server and can be overloaded in each virtual host :

| Name                           | Description                                     |
| ------------------------------ | ----------------------------------------------- |
| `apache2__serveradmin`         | The optionnal email address of the administrator|
| `apache2__allow_override_list` | The AllowOverrideList directive                 |
| `apache2__allow_override`      | The AllowOverride directive                     |
| `apache2__options`             | The Option directive                            |

To configure which module are enabled or not, you must declare all module's name in any of the following three lists :

* apache2__modules_enabled_global
* apache2__modules_enabled_group
* apache2__modules_enabled_host

By default, no any module is enabled, so be noticed that apache will not stard without any of mpm module enabled.
Each entry in theses list must be the module name. In case where a module have a '.conf' and a '.load' file, they will be automatically included as possible. In addition, if the role contains a template file in templates/modules.conf/(module name) directory it will replace any existing distribution's configuration file.

### Virtual hosts

Each virtual host must be declared with a vhost block. You can put a vhost block into any of the three available lists

* apache2__virtual_hosts_global
* apache2__virtual_hosts_group
* apache2__virtual_hosts_host

By default each virtual host listen on '*' and on the default port identified according to the HTTP(s) status.
If SSL Engine is 'ON' it uses 443, otherwise 80.

Only a subset of apache2 directives and sections are implemented in ansible, you can see available in files [directives](templates/_directives.j2) [sections](templates/_sections.j2). If you need a directive that is not implemented, you can use the extra_parameters items. But if a sections type is missing, you need to fork and implement it in the role.

Each vhost block must be put in a dict where the key will be the filename of the vhost configuration. Then each vhost must be a dict which can contains theses variables :

| Name                        | Type                          | Description                                                                                                                                                                  |
| --------------------------- | ------------------------------| -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| hosts                       | string or array of string/dict| list of interface on which the vhost will listen                                                                                                                             |
| hosts[]                     | string                        | if an item of the hosts list is a string it will be interpreted as "IP:PORT" or "X.X.X.X:X"                                                                                  |
| hosts[].ip                  | string                        | if an item of the hosts list is a dict with 'ip' key, it will be interpreted as "IP"                                                                                         |
| hosts[].port                | int                           | if an item of the hosts list is a dict with 'port' key, it will be used as listen port. If this key is not set, it will be deducted from HTTP protocol (see above)           |
| server_name                 | string                        | the host of the vhost                                                                                                                                                        |
| server_alias                | string                        | the hostname alias                                                                                                                                                           |
| server_admin                | string                        | the optionnal administrator email address                                                                                                                                    |
| document_root               | string                        | The path to the document root folder. This directory will be automaticallly created, because Apache won't start if it is missing.                                            |
| document_root_user          | string                        | The unix owner of the document root folder. This is only applied if the variable is defined                                                                                  |
| document_root_group         | string                        | The unix group of the document root folder.This is only applied if the variable is defined                                                                                   |
| document_root_mode          | string                        | The unix mode of the document root folder. This is only applied if the variable is defined. Take care that apache still have access to this folder at least in read only mode|
| error_log                   | string                        | The path to the error log file. The error log file will be created in this directory, so please ensure apache still sufficients have access rights                           |
| error_log_user              | string                        | The unix owner of the error log directory                                                                                                                                    |
| error_log_group             | string                        | The unix group of the error log directory                                                                                                                                    |
| allow_override              | string                        | The AllowOverride directive                                                                                                                                                  |
| allow_override_list         | string                        | The AllowOverrideList directive                                                                                                                                              |
| options                     | string                        | The Option directive                                                                                                                                                         |
| headers                     | array                         | Array of Header directive                                                                                                                                                    |
| files_match                 | array of dict (see below)     | Contains FileMatch definition, each one must be a dict with following keys                                                                                                   |
| files_match[].regexp        | string                        | The regular expression that triggers the file match                                                                                                                          |
| files_match[].actions       | array of string               | The list of Apache directive to execute when this file match is triggered                                                                                                    |
| extra_parameters            | array of string               | Any extra Apache directives                                                                                                                                                  |
| https                       | dict                          | see below for all https subkey                                                                                                                                               |
| https.enabled               | boolean                       | True by default, can be use to disable https and preserve configurations string                                                                                              |
| https.certificate_chain_file| string                        | The path to the certificate chain                                                                                                                                            |
| https.verify_client         | string                        | The type of client certificate verification to perform                                                                                                                       |
| https.verify_client_depth   | int                           | The maximum depth for client certificate verification                                                                                                                        |
| https.ca_certificate_path   | string                        | The path to the CA certificate directory                                                                                                                                     |
| https.ca_certificate_file   | string                        | The path to the CA certificate file                                                                                                                                          |
| https.crl_path              | string                        | The path to the CRL folder                                                                                                                                                   |
| https.crl_file              | string                        | The path to the CRL file                                                                                                                                                     |

## Facts

By default the local fact are installed and expose the following variables :

* ```ansible_local.apache2.version_full```
* ```ansible_local.apache2.version_major```


## Example

### Playbook

Use it in a playbook as follows:

```yaml
- hosts: all
  roles:
    - turgon37.apache2
```

### Inventory

  * Example of manually loaded apache modules

```
apache2__modules_enabled_group:
  - access_compat # provide supports for old directives Allow,Order that are deprecated
  - alias  # provide  Alias
#  - auth_basic  # provide Basic HTTP auth
  - authn_core
#  - authn_file  # auth based on htpasswd
  - authz_core
#  - authz_host  # auth based on ip/host
#  - authz_user  # auth based on username
#  - autoindex  # disabled, indexes are disabled
  - deflate # provide Gzip compression
  - dir # provide  DirectoryIndex
  - env  # provide SetEnv
#  - filter  # provide FilterChain
  - headers  # provide RequestHeader
  - mime
  - mpm_prefork
  - negotiation # handle Content Type
  - php7.0
#  - proxy
#  - proxy_http
#  - setenvif
  - ssl  # Handle SSL
  - socache_shmcb  # required by mod_ssl
```

  * Default debian virtual host

```
apache2__host_virtual_hosts:
  000-default:
    server_name: www.example.com
    server_admin: webmaster@localhost
    document_root: /var/www/html
    sections:
      - type: directory
        path: /var/www/html
        directives:
          - require: all granted
    error_log: '{{ apache2__log_directory }}/error.log'
    custom_log: '{{ apache2__log_directory }}/access.log combined'
```


  * Simple permanent redirect from HTTP to HTTPs

```
apache2__host_virtual_hosts:
  web-redirect:
    hosts:
      - ip: "10.0.0.1"
    server_name: www.example.net
    server_alias: www2.example.net
    extra_parameters:
      - RedirectPermanent / https://www.example.net/
```

  * Proxy pass from HTTPs to HTTP

```
apache2__host_virtual_hosts:
  proxy-https:
    hosts:
      - ip: 10.0.0.1
      - ip: 192.168.56.12
    server_name: www.example.net
    server_alias: www2.example.net
    extra_parameters:
      - 'ProxyRequests Off'
      - 'ProxyPreserveHost On'
      - 'ProxyPass / http://localhost:3001/'
      - 'ProxyPassReverse / https://localhost:3001/'
    https:
      certificate_file: /etc/ssl/apache2/www.example.net.pem
      certificate_key_file: /etc/ssl/apache2/www.example.net.key
```

  * HTTP virtual host with document root and a PHP application (Jeedom)

```
apache2__host_virtual_hosts:
    hosts:
      - 10.0.0.1
      - "127.0.0.1:443"
    server_name: jeedom.example.net
    document_root: /var/www/html
    document_root: '{{ jeedom__install_directory }}'
    document_root_user: '{{ apache2__service_user }}'
    document_root_group: '{{ apache2__service_user }}'
    error_log: '{{ jeedom__install_directory }}/log/http.error'
    error_log_user: '{{ apache2__service_user }}'
    error_log_group: '{{ apache2__service_user }}'
    sections:
      - type: directory
        path: '{{ jeedom__install_directory }}'
        directives:
          - allow_override: All
          - options: -Indexes -ExecCGI -FollowSymLinks
          - require: all granted
      - type: files_match
        regex: '\.(appcache|atom|bbaw|bmp|crx|css|cur|eot|f4[abpv]|flv|geojson|gif|htc|ico|jpe?g|js|json(ld)?|m4[av]|manifest|map|mp4|oex|og[agv]|opus|otf|pdf|png|rdf|rss|safariextz|svgz?|swf|topojson|tt[cf]|txt|vcard|vcf|vtt|webapp|web[mp]|webmanifest|woff2?|xloc|xml|xpi)$'
        directives:
          - header:
              - unset Content-Security-Policy
              - unset X-Frame-Options
              - unset X-XSS-Protection
    directives:
      - header:
          # Content Security Policy (CSP)
          #- set Content-Security-Policy "script-src 'self'; object-src 'self'"
          # Reducing MIME type security risks
          - set X-Content-Type-Options "nosniff"
          # Clickjacking
          - set X-Frame-Options "DENY"
          # Reflected Cross-Site Scripting (XSS) attacks
          - set X-XSS-Protection "1; mode=block"
          - unset X-Powered-By
```

  * HTTPs virtual host with document root and a PHP application (Jeedom)


```
apache2__host_virtual_hosts:
  jeedom-https:
    hosts:
      - ip: 10.0.0.1
      - ip: 127.0.0.1
        port: 4343
    server_name: jeedom.example.net
    document_root: /var/www/html
    allow_override: All
    options: '-Indexes -ExecCGI -FollowSymLinks'
    headers:
      - set X-Content-Type-Options "nosniff"
      - always set Strict-Transport-Security "max-age=16070400; includeSubDomains"
      - set X-XSS-Protection "1; mode=block"
      - unset X-Powered-By
    files_match:
      - regexp: '\.(appcache|atom|bbaw|bmp|crx|css|cur|eot|f4[abpv]|flv|geojson|gif|htc|ico|jpe?g|js|json(ld)?|m4[av]|manifest|map|mp4|oex|og[agv]|opus|otf|pdf|png|rdf|rss|safariextz|svgz?|swf|topojson|tt[cf]|txt|vcard|vcf|vtt|webapp|web[mp]|webmanifest|woff2?|xloc|xml|xpi)$'
        actions:
          - Header unset Content-Security-Policy
          - Header unset X-Frame-Options
          - Header unset X-XSS-Protection
    https:
      certificate_file: /etc/ssl/apache2/jeedom.www.example.net.pem
      certificate_key_file: /etc/ssl/apache2/jeedom.www.example.net.key
```
