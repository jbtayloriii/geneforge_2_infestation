# Geneforge game site

## Installation

1. Set up a virtual environment and activate it

`python3.14 -m venv .venv`
`source .venv/bin/activate`

2. Install the dependencies from `requirements.txt`

`python3 -m pip install -r requirements.txt`

# Running

The flask CLI can run the backend:

`flask -A src/app.py run --debug`
