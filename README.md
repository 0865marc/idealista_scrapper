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
- redis-server

### Installing Redis Server on Ubuntu 24.04.2 LTS WSL

#### Installing Redis Server
```bash
sudo apt-get install redis-server
```

#### Starting Redis Server
```bash
sudo service redis-server start
```

#### Checking Redis Server Status
```bash
sudo service redis-server status
```
