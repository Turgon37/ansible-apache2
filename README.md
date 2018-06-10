Ansible Role Apache2
========

[![Build Status](https://travis-ci.org/Turgon37/ansible-apache2.svg?branch=master)](https://travis-ci.org/Turgon37/ansible-apache2)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-Turgon37.apache2-blue.svg)](https://galaxy.ansible.com/Turgon37/apache2/)

:warning: This role is under development, some important (and possibly breaking) changes may happend. Don't use it in production level environments but you can eventually base your own role on this one :hammer:

:grey_exclamation: Before using this role, please know that all my Ansible roles are fully written and accustomed to my IT infrastructure. So, even if they are as generic as possible they will not necessarily fill your needs, I advice you to carrefully analyse what they do and evaluate their capability to be installed securely on your servers.

Require Ansible >= 2.4


This roles configures an instance of Apache2 daemon

## OS Family

This role is available for Debian

## Features

At this day the role can be used to configure :

  * Apache2 main server configuration file
  * Listens directives to restrict apache listening to vhost defined ports only
  * multiple virtual hosts
  * list of enabled/disable apaches modules

## Configuration

### Server

The following variable apply to the all server :

| Name                        | Description                                                                       |
| --------------------------- | --------------------------------------------------------------------------------- |
| apache2__server_tokens      | Configure the verbosity of the server token in error pages                        |
| apache2__server_signature   | Print or not the server signature on error pages                                  |
| apache2__trace_enable       | Configure the HTTP TRACE method                                                   |
| apache2__ssl_ciphers        | List the available SSL ciphers, by default only a recommanded subset is configured|
| apache2__ssl_protocols      | List the enabled SSL protocols, by default all except SSL 2/3                     |
| apache2__ssl_honorciphers   | Tell to server to prefer the cipher order                                         |

The following variable apply to server and can be overloaded in each virtual host :

| Name                         | Description                                     |
| ---------------------------- | ----------------------------------------------- |
| apache2__serveradmin         | The optionnal email address of the administrator|
| apache2__allow_override_list | The AllowOverrideList directive                 |
| apache2__allow_override      | The AllowOverride directive                     |
| apache2__options             | The Option directive                            |

To configure which module are enabled or not, you must declare all module's file name in any of the three list :

* apache2__global_modules_enabled
* apache2__group_modules_enabled
* apache2__host_modules_enabled

Each name of theses list muse contains the module name and the file's extension. In case where a module have a '.conf' and a '.load' file, you have to put theses two name in the list.

### Virtual hosts

Each virtual host must be declared with a vhost block. You can put a vhost block into any of the three available lists

* apache2__global_virtual_hosts
* apache2__group_virtual_hosts
* apache2__host_virtual_hosts

By default each virtual host listen on '*' and on the default port identified according to the HTTP(s) status.
If SSL Engine is 'ON' it uses 443, otherwise 80.


Each vhost block must be put in a dict where the key will be the filename of the vhost configuration. Then each vhost must be a dict which can contains theses variables :

| Name                        | Type                          | Description                                                                                                                                                       |
| --------------------------- | ------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| hosts                       | string or array of string/dict| list of interface on which the vhost will listen                                                                                                                  |
| hosts[]                     | string                        | if an item of the hosts list is a string it will be interpreted as "IP:PORT" or "X.X.X.X:X"                                                                       |
| hosts[].ip                  | string                        | if an item of the hosts list is a dict with 'ip' key, it will be interpreted as "IP"                                                                              |
| hosts[].port                | int                           | if an item of the hosts list is a dict with 'port' key, it will be used as listen port. If this key is not set, it will be deducted from HTTP protocol (see above)|
| servername                  | string                        | the host of the vhost                                                                                                                                             |
| serveralias                 | string                        | the hostname alias                                                                                                                                                |
| serveradmin                 | string                        | the optionnal administrator email address                                                                                                                         |
| documentroot                | string                        | The path to the document root folder                                                                                                                              |
| allow_override              | string                        | The AllowOverride directive                                                                                                                                       |
| allow_override_list         | string                        | The AllowOverrideList directive                                                                                                                                   |
| options                     | string                        | The Option directive                                                                                                                                              |
| headers                     | array                         | Array of Header directive                                                                                                                                         |
| files_match                 | array of dict (see below)     | Contains FileMatch definition, each one must be a dict with following keys                                                                                        |
| files_match[].regexp        | string                        | The regular expression that triggers the file match                                                                                                               |
| files_match[].actions       | array of string               | The list of Apache directive to execute when this file match is triggered                                                                                         |
| extra_parameters            | array of string               | Any extra Apache directive                                                                                                                                        |
| https                       | dict                          | see below for all https subkey                                                                                                                                    |
| https.enabled               | boolean                       | True by default, can be use to disable https and preserve configurations string                                                                                   |
| https.certificate_chain_file| string                        | The path to the certificate chain                                                                                                                                 |
| https.verify_client         | string                        | The type of client certificate verification to perform                                                                                                            |
| https.verify_client_depth   | int                           | The maximum depth for client certificate verification                                                                                                             |
| https.ca_certificate_path   | string                        | The path to the CA certificate directory                                                                                                                          |
| https.ca_certificate_file   | string                        | The path to the CA certificate file                                                                                                                               |
| https.crl_path              | string                        | The path to the CRL folder                                                                                                                                        |
| https.crl_file              | string                        | The path to the CRL file                                                                                                                                          |


### Example

  * Example of fully loaded module apache

```
apache2__host_modules_enabled: ['access_compat.load', 'alias.conf', 'alias.load', 'auth_basic.load', 'authn_core.load', 'authn_file.load', 'authz_core.load', 'authz_host.load', 'authz_user.load', 'headers.load', 'autoindex.conf', 'autoindex.load', 'deflate.conf', 'deflate.load', 'dir.conf', 'dir.load', 'env.load', 'filter.load', 'mime.conf', 'mime.load', 'mpm_prefork.conf', 'mpm_prefork.load', 'negotiation.conf', 'negotiation.load', 'php5.conf', 'php5.load', 'proxy.load', 'proxy_http.load', 'setenvif.conf', 'setenvif.load', 'ssl.load', 'ssl.conf', 'socache_shmcb.load']
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
    servername: www.example.net
    serveralias: www2.example.net
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
    servername: www.example.net
    serveralias: www2.example.net
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
  jeedom:
    hosts:
      - 10.0.0.1
      - "127.0.0.1:443"
    servername: jeedom.example.net
    documentroot: /var/www/html
    allow_override: All
    options: '-Indexes -ExecCGI -FollowSymLinks'
    headers:
      - set X-Content-Type-Options "nosniff"
      - set X-XSS-Protection "1; mode=block"
      - unset X-Powered-By
    files_match:
      - regexp: '\.(appcache|atom|bbaw|bmp|crx|css|cur|eot|f4[abpv]|flv|geojson|gif|htc|ico|jpe?g|js|json(ld)?|m4[av]|manifest|map|mp4|oex|og[agv]|opus|otf|pdf|png|rdf|rss|safariextz|svgz?|swf|topojson|tt[cf]|txt|vcard|vcf|vtt|webapp|web[mp]|webmanifest|woff2?|xloc|xml|xpi)$'
        actions:
          - Header unset Content-Security-Policy
          - Header unset X-Frame-Options
          - Header unset X-XSS-Protection
```

  * HTTPs virtual host with document root and a PHP application (Jeedom)


```
apache2__host_virtual_hosts:
  jeedom-https:
    hosts:
      - ip: 10.0.0.1
      - ip: 127.0.0.1
        port: 4343
    servername: jeedom.example.net
    documentroot: /var/www/html
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
