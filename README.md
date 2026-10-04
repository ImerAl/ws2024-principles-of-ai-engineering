# WS2024 — Principles of AI Engineering

An issue-ticket classifier built for the *Principles of AI Engineering*
course (WS2024). It predicts the category of a support ticket
(**bug**, **enhancement** or **question**) from its title and body using a
**Random Forest** model, and serves the prediction through a small
**Flask** web application.

## Overview

Users submit a ticket title and description through a web form. The text is
preprocessed, its language is verified to be English, and a trained
scikit-learn pipeline predicts a category. Every prediction is stored in a
MySQL database so it can later be reviewed and manually corrected, and the
model exposes Prometheus metrics that can be scraped and visualized with
Grafana.

## Features

- **Ticket classification** with a Random Forest classifier
  (scikit-learn).
- **Text preprocessing** pipeline: lowercasing, accent/emoji removal,
  punctuation stripping, tokenization (NLTK), stop-word removal and Porter
  stemming.
- **Language detection** (`langdetect`) — only English text is classified.
- **Web interface** to submit a ticket and see/correct the predicted label.
- **Persistence in MySQL**: predictions are stored and can be corrected
  (`/api/correct`), which also feeds the quality metrics.
- **Observability**: Prometheus metrics exposed at `/metrics` plus a
  Prometheus + Grafana stack via `docker-compose`.
- **Tests** with `pytest`.

## How it works

1. The user posts a `title` and a `description` to `/api/predict`.
2. The text is preprocessed (`flaskr/text_preprocessing.py`) and its
   language is checked. Non-English input is rejected.
3. The preprocessed title and body are passed to the model
   (`flaskr/model.py`), which applies two TF-IDF vectorizers (one for the
   title, one for the body) and a `RandomForestClassifier`.
4. The prediction is stored in MySQL (`flaskr/connection.py`) and returned
   to the page.
5. If the prediction is wrong, the user selects the correct label, which
   updates the database and adjusts the Prometheus counters/gauges.

### Model pipeline

```python
Pipeline(steps=[
    ("preprocessor", ColumnTransformer([
        ("text1", TfidfVectorizer(), "token_title"),
        ("text2", TfidfVectorizer(), "token_body"),
    ])),
    ("classifier", RandomForestClassifier(random_state=42)),
])
```

The trained artifacts are saved with `joblib` as
`issue_classifier.pkl` and `vectorizer.pkl` (see
`flaskr/train_model_code.py`).

## Project structure

```
flaskr/
  __init__.py            # Flask app, routes and Prometheus metrics
  connection.py          # MySQL create / read / select / update helpers
  model.py               # Loads the .pkl model and predicts / computes confidence
  predict.py             # Preprocessing + prediction orchestration
  text_preprocessing.py  # Cleaning, tokenization, stop-words, stemming, lang detection
  train_model_code.py    # Training script for the Random Forest pipeline
  generate_id.py         # Ticket ID generator
  static/                # CSS, notebooks and (local) model/data files
  Templates/index.html   # Web form and correction UI
prometheus/prometheus.yml
docker-compose.yaml      # Prometheus + Grafana services
tests/test__init__.py    # pytest tests
```

## Requirements

- Python 3.12
- Flask, scikit-learn, pandas, numpy, nltk, langdetect, joblib,
  mysql-connector-python, prometheus-client (see `requirements.txt`)
- A running MySQL server
- Docker (optional, for Prometheus/Grafana)

## Installation

```bash
# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Configuration

### Database

Create a MySQL database named `text_prediction` with a table `text_store`
holding at least the columns `id_ticket`, `category`, `title` and
`description`, then adjust the credentials in `flaskr/connection.py`:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="text_prediction",
)
```

### Model and data files

The trained model (`issue_classifier.pkl`), the vectorizer
(`vectorizer.pkl`) and the CSV datasets are **not** versioned (they are
listed in `.gitignore` because of their size). Generate them locally with
the training script before running the app:

```bash
python -m flaskr.train_model_code
```

This produces `issue_classifier.pkl`, `vectorizer.pkl` and
`prediction.csv` inside the working directory / `flaskr/static/`.

## Running the app

```bash
flask --app flaskr:flask_app run
```

Then open <http://127.0.0.1:5000/> and submit a ticket.

## API / Endpoints

| Method | Route          | Description                                              |
|--------|----------------|----------------------------------------------------------|
| GET    | `/`            | Web form                                                 |
| GET    | `/<name>`      | Simple greeting (`Hello <name>!`)                        |
| POST   | `/api/predict` | Classifies a ticket (`title`, `description` form fields) |
| POST   | `/api/correct` | Stores the corrected label for a ticket (`id`, `radio`)  |
| GET    | `/metrics`     | Prometheus metrics                                       |

## Monitoring

Start Prometheus and Grafana:

```bash
docker compose up -d
```

- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>

Prometheus scrapes the Flask app at `host.docker.internal:5000/metrics`.
The exposed metrics include `accuracy`, `avg_pred_confidence`,
`preds_per_category`, `correct_preds_per_category` and
`incorrect_preds_per_category`.

## Tests

```bash
pytest
```

## Authors

ImerAl — *Principles of AI Engineering*, University of Passau (WS2024).

## License

For academic use.
