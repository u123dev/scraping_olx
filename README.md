### Scraping Site olx

This project scrapes ads listings from website olx and saves it to database.

### Features:
- Scrapy framework.

  For accessing some fields (ex. phones) used internal olx api.
 
  It is strongly recommended to use proxy to avoid ip blocking when there is a large flow of requests.


- Scraping App starts every 1 min. 
  It analyzes the first 5 website pages to find the new created ads to save.

- Dumping db starts daily at 12 am (timezone=Europe/Kiev) as a separate process. 
  Path to dumps in root: ```dumps/```

- Configured Logging system for log file rotation (5 files each 1Gb).
  Path to logs - in root


Applications are deployed in docker containers:
- scrapy apps volume
- celery worker for scraping
- celery worker for dumping
- celery beat cron scheduler
- flower tasks monitoring
- redis as broker
- postgresql db
- db data volume

___
### Tech Stack & System requirements :

* Python 3.1+
* Scrapy 
* SqlAlchemy orm
* Alembic 
* PostgreSQL Database 
* Celery
* Redis (used as a Broker & Backend)
* Flower (monitoring for Celery)
* Docker Containerization

---

### Run with Docker containers
 System requirements:

* **Docker Desktop 4.+**

Run project:
```
docker-compose up --build
```

Please note:
   * Copy [.env-sample](.env-sample) file to **.env** & set environment variables 


#### Tasks monitoring - Access Flower / Celery tasks monitoring
   - [http://127.0.0.1:5555/tasks/](http://127.0.0.1:8000/5555/tasks/)

### Contact
Feel free to contact: u123@ua.fm
