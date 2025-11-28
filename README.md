#  🐍  FastAPI Internet of Things (IoT) Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-009688.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-enabled-2496ED.svg)](https://www.docker.com/)

---

## 📝 Overview / معرفی

This project is a **FastAPI backend** for managing IoT sensors and units.  
It provides CRUD operations for **units**, **sensors**, and **readings**, integrates with PostgreSQL, and is fully containerized using Docker.

این پروژه یک بک‌اند **FastAPI** برای مدیریت سنسورها و واحدهای IoT است.  
عملیات CRUD برای واحدها، سنسورها و داده‌های سنسورها فراهم شده و پروژه با PostgreSQL کار می‌کند و به طور کامل با Docker کانتینریزه شده است.

---

## 🚀 Project Overview | نمای کلی پروژه

- Backend API for IoT sensor management using **FastAPI** and **PostgreSQL**  
- CRUD operations for:
  - Units
  - Sensors
  - Sensor Readings  
- Repository Pattern (No ORM)
- Swagger & Redoc documentation
- Unit testing
- Dockerized deployment with sample seed data
---
- API بک‌اند برای **مدیریت سنسورهای IoT** با استفاده از **FastAPI** و **PostgreSQL**  
- قابلیت‌های CRUD برای:
  - واحدها
  - سنسورها
  - داده‌های سنسورها  
- استفاده از الگوی Repository (بدون ORM)
- مستندات Swagger و Redoc
- تست‌های خودکار
- اجرای کامل با Docker و داده‌های اولیه (seed)

---

## 🛠️ تکنولوژی‌های استفاده شده

| بخش | تکنولوژی |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| DB Access | Repository Pattern (بدون ORM) |
| Container | Docker + Docker Compose |
| Testing | Pytest |
| Docs | `/docs` (Swagger) + `/redoc` |
| Dependency Management | requirements.txt |

---

## ✨ Features / ویژگی‌ها
- ✅ CRUD APIs for **Unit**, **Sensor**, **Reading**
- ✅ PostgreSQL connection using **Repository Pattern** (No ORM)
- ✅ OpenAPI docs available at `/docs` `/redoc`
- ✅ Unit tests with pytest
- ✅ Fully containerized with Docker & docker-compose  & production-ready
- ✅ Automatic seed/sample data on startup
- ✅ Clean Architecture + Domain Driven Design
- ✅ Environment-based config

---

## 📂 Project Structure | ساختار پروژه

```
📦 FastAPI-internet-of-things
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── main.py
├── pyproject.toml
├── requirements.txt
├── README.md
│
├── 📁 app
│ ├── main.py
│ ├── exceptions.py
│ │
│ ├── 📁 api
│ │ ├── deps.py
│ │ └── 📁 routers
│ │ ├── readings.py
│ │ ├── sensors.py
│ │ └── units.py
│ │
│ ├── 📁 core
│ │ ├── config.py
│ │ └── pyd.py
│ │
│ ├── 📁 db
│ │ ├── init_database.py
│ │ ├── schema.py
│ │ ├── seed.py
│ │ ├── seed_run.py
│ │ └── session.py
│ │
│ ├── 📁 domain
│ │ ├── reading.py
│ │ ├── sensor.py
│ │ └── unit.py
│ │
│ ├── 📁 repositories
│ │ ├── reading.py
│ │ ├── sensor.py
│ │ └── unit.py
│ │
│ └── 📁 schemas
│ ├── reading.py
│ ├── sensor.py
│ └── unit.py
│
└── 📁 tests
├── conftest.py
├── test_config.py
├── test_health.py
├── test_integrity.py
├── test_integrity_simple.py
├── test_readings_api.py
├── test_sensors_api.py
└── test_units_api.py

```


---

## ⚙️ Setup & Installation | نصب و راه‌اندازی

### Clone the project | دریافت پروژه
```bash
git clone https://github.com/yourusername/FastAPI-internet-of-things.git
cd FastAPI-internet-of-things
```
##  🔧  پیش‌نیازها | Requirements

- Python 3.7+
- Docker & Docker Compose (برای اجرای کانتینری)
- یا PostgreSQL و محیط لوکال (در صورت عدم استفاده از Docker)


### Local environment | نصب لوکال
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

## 🌐 **Environment Variables / متغیرهای محیطی**

- `DATABASE_URL` – PostgreSQL connection string  
- `ENV` – environment (`prod`, `test`, `dev`)

**Example for Docker Compose:**

```yaml
environment:
  DATABASE_URL: postgresql+psycopg2://fastapi:fastapi@db:5432/iot_db
  ENV: prod
```

___

## 🐳 اجرای پروژه با Docker

### ⚡ راه‌اندازی دیتابیس و مقداردهی اولیه

 1️⃣ اجرای دیتابیس روی Docker 
```bash
docker-compose up -d db
```

* سرویس `db` در docker-compose.yml به عنوان PostgreSQL اجرا می‌شود.
* برای مقداردهی اولیه (Sample Data) از ماژول `app.db.seed_run` استفاده می‌شود:

```bash
docker compose run seed
```

* متغیرهای محیطی مهم:

  ```env
  ENV=prod
  DATABASE_URL=postgresql+psycopg2://fastapi:fastapi@db:5432/iot_db
  ```

---



2️⃣ ساخت و اجرای کانتینرها:

```bash
docker compose up --build
```


---


## ☁️ اجرای پروژه در Local
 1️⃣ مقداردهی اولیه 
```bash
python -m app.db.seed_run
```
___
2️⃣ اجرای پروژه

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
___

This starts:

🗄 PostgreSQL database (db service)

🌱 Seed data (seed service)

🚀 FastAPI app (web service) at http://localhost:8000



___
### 🧬 Generate/Update requirements.txt
```bash
pip freeze > requirements.txt
```

___

## 📦 Access Swagger / مستندات OpenAPI
http://localhost:8000/docs

http://localhost:8000/redoc

---
## 🧪 Running Tests / اجرای تست‌ها
###
🎯 Testing Strategy
* Use  a **test database** to isolate tests from production data

* No connection to production PostgreSQL during test runs


* Negative & positive scenario coverage
###  Use pytest inside the container:
```bash
docker compose exec web pytest
```

###  Use pytest in local
```bash
pytest -v
```

___

## 🧠 Key Design Notes

* ❗ No ORM was used — raw SQL via Repository Pattern.
* Business logic isolated inside Service layer.
* Domain objects encapsulate behavior (rename(), update_value() etc.)
* Errors unified via custom exceptions (NotFoundError, ForeignKeyError, ...)

___

## 📝 API Endpoints

### Units

* `GET /units/` — دریافت لیست واحدها
* `POST /units/` — ایجاد واحد جدید
* `GET /units/{id}` — دریافت جزئیات یک واحد
* `PUT /units/{id}` — بروزرسانی واحد
* `DELETE /units/{id}` — حذف واحد
* `GET /units/{id}/overview` — دریافت یک نمای خلاصه از وضعیت Unit شامل:
  - نام و نماد Unit
  - تعداد سنسورهای مرتبط (`sensor_count`)
  - تعداد کل Readings ثبت‌شده (`reading_count`)
  - آخرین مقدار ثبت‌شده (`latest_readings`) به‌صورت لیست شامل:
    - `sensor_id`
    - `value`
    - `observed_at`

### Sensors

* `GET /sensors/` — دریافت لیست سنسورها
* `POST /sensors/` — ایجاد سنسور جدید
* `GET /sensors/{id}` — دریافت جزئیات سنسور
* `PUT /sensors/{id}` — بروزرسانی سنسور
* `DELETE /sensors/{id}` — حذف سنسور

### Readings

* `GET /readings/` — دریافت لیست Readings
* `POST /readings/` — ایجاد Reading جدید
* `GET /readings/{id}` — دریافت جزئیات Reading
* `PUT /readings/{id}` — بروزرسانی Reading
* `DELETE /readings/{id}` — حذف Reading

تمام Endpoints با استفاده از OpenAPI مستندسازی شده‌اند و از طریق `/docs` قابل مشاهده هستند.

---


## 📌 Notes / نکات

  - All DB access is via Repository Pattern — No ORM used.
  - IDs are auto-generated by PostgreSQL.
  - Foreign key and unique constraints are handled in the service layer.
  - All services (UnitService, SensorService, ReadingService) are implemented and tested.


  - پروژه بدون ORM است و تمام ارتباط با دیتابیس از طریق **Repository Pattern** انجام می‌شود.
  - همه‌ی ID‌ها توسط پایگاه داده تولید می‌شوند (Auto Increment).
  - محدودیت‌های کلید خارجی و یونیک در لایه سرویس مدیریت می‌شوند.
  - تمام سرویس‌ها (UnitService, SensorService, ReadingService) پیاده‌سازی شده و تست شده‌اند.
---

## 🧩 خلاصه

این پروژه آماده‌ی اجرای **کانتینری** و **لوکال** است، دارای:

* FastAPI + PostgreSQL
* CRUD کامل برای Units, Sensors, Readings
* مستندات OpenAPI
* تست‌های pytest
* Dockerfile و docker-compose.yml


---


``` js
 █████   ██   ██  █████    ██████   █████    ██   ██  ███████  ███████  ██   ██
██        ██ ██   ██  ██   ██       ██  ██   ███  ██    ███      ███    ██   ██
██         ███    █████    █████    █████    ██ █ ██    ███      ███    ███████
██          █     ██  ██   ██       ██ ██    ██  ███    ███      ███    ██   ██
██          █     ██  ██   ██       ██  ██   ██   ██    ███      ███    ██   ██
 █████      █     █████    ██████   ██   ██  ██   ██  ███████    ███    ██   ██

                    C Y B E R N I T H
                 
> ⚡ Crafted & unleashed by Soroosh morshedi ~ ( Cybernith ) ~
>  🌐  https://sorooshmorshedi.ir
> ❤️ Built with passion 
```


