# Idealista Scrapper

A FastAPI backend service that provides access to real estate data from Idealista.

## Overview

This project consists of two main components:
1. A scraping process that collects real estate data from Idealista
2. A FastAPI backend that serves the collected data through REST APIs

## Features

- Automated data collection from Idealista listings
- RESTful API endpoints to query real estate data
- Structured storage of property information
- Configurable scraping parameters

## Requirements
- Ubuntu 24.04.2 LTS
- uv
- ruff
- supervisor
- redis-server


#### Installing Redis Server
```bash
sudo apt-get install redis-server
```

#### Installing Supervisor
```bash
sudo apt-get install supervisor
```

#### Run it once to create /var/run/supervisor.sock
```bash
sudo supervisord -c /etc/supervisor/supervisord.conf
```

#### Create logs directories
```bash
sudo mkdir -p /var/log/redis
sudo mkdir -p /var/log/celery
```

#### Set correct permissions
```bash
sudo chown -R redis:redis /var/log/redis
sudo chown $USER:$USER /var/log/celery   #use your user instead of $USER
```

#### Configuring Supervisor
```bash
sudo nano /etc/supervisor/conf.d/idealista_scraper.conf
```

```
[program:redis]
priority=10
command=/usr/local/bin/redis-server /etc/redis/redis.conf
user=redis
autostart=true
autorestart=true
stdout_logfile=/var/log/redis/stdout.log
stderr_logfile=/var/log/redis/stderr.log

[program:celery-worker]
priority=20
command=/ruta/entorno/bin/celery -A test_celery.celery_app worker --loglevel=INFO
directory=/ruta/proyecto
user=usuario
autostart=true
autorestart=true
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker-error.log

[group:celery-sistema]
programs=redis,celery-worker
```

#### Restart Supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start idealista_scraper
```

#### Check status
```bash
sudo supervisorctl status
```
