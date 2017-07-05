Unifi controller
=========

A role for installing the unifi controller service on CentOS

Requirements
------------

None.

Role Variables
--------------

defaults in defaults/main.yml
* `unifi_zip_destination: '/tmp/unifi.zip'` The location where the source zip file will be downloaded on the server executing the ansible role
* `unifi_install_destination: '/opt'` The path where unifi will be installed to. Will create a directory called `UniFi`
* `unifi_download_url: 'https://www.ubnt.com/downloads/unifi/5.0.6/UniFi.unix.zip'` The URL to the unifi zip
* `unifi_user: unifi` The user that will used for running the service
* `mongod_path: '/usr/bin/mongod'` The path where mongod is located when installed
* `unifi_service_port: 8000` The port the service will use

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: unifi_controller
      roles:
         - { role: peerster.unifi_controller }

License
-------

BSD

Author Information
------------------

Created 2016 by [peerster](https://github.com/peerster)
