# Dependencies
- Python 3.10+

# Setup

- Create a virtual python environment \
    ``` python -m venv .venv ```

- Activate the virtual environment
    - Windows: ``` .venv\Scripts\activate ```
    - Linux / Mac: ``` source .venv/bin/activate ```

- Install required packages \
    ``` pip install -r requirements.txt ```

# How to run
- Run the Flask app \
    ``` python -m flask run -h 127.0.0.1 -p 5000 ```

# How to test
- Run the Flask app
- While the Flask app is running, start the test \
    ``` python -m pytest ```