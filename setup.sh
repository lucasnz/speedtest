#!/bin/bash
rm -rf db_config/
rm -rf db_data/
rm -rf grafana_config/

mkdir grafana_config/
chown 573:65533 grafana_config/
chmod 700 grafana_config/
chmod 755 db_scripts/*
