#! /bin/bash

COMMAND='
CREATE DATABASE ipm_database;
USE ipm_database;
CREATE TABLE ipm_table (ip_address VARCHAR(255), hostname VARCHAR(255), note VARCHAR(255) );
INSERT INTO ipm_table (ip_address, hostname, note) VALUES ("192.168.3.100", "IchiNUC", "HostOS");
'

mysql --user=root --password=Ichi2116 --execute="$COMMAND"

