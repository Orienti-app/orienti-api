# OrientiApi

API for Orienti.app originally developed during small a hackathon in the end of September 2021.

## Installation

We use

- [poetry](https://python-poetry.org/) for dependency management
- [PostgreSQL](https://www.postgresql.org/) (10+) as relational a data storage
- [MongoDB](https://www.mongodb.com/) as storage for sync

- To set up instance with demo database follow these simple steps:

1. Create python virtual environment (`python -m venv venv`)
2. Enter environment (`source venv/bin/activate`)
3. Install dependencies `poetry install`
4. Create `.env` file according `.env.example`
5. Execute migrations `python manage.py migrate`
6. Create superuser using `python manage.py createsuperuser`

---
Made with ❤️ ☕ & 🍺️ Orienti.app team
