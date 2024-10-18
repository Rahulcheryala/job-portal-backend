# Project Setup

This README will guide you through setting up the environment and running the Django project.

## Prerequisites

Before you start, ensure you have Python and pip installed on your system.

## Setup

1. **Activate Virtual Environment** (optional but recommended):

    ```bash
    source <path_to_virtualenv>/bin/activate
    ```

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Migrate Database**:

    ```bash
    python manage.py migrate
    ```

## Run the Server

To start the development server, run:

```bash
python manage.py runserver
```