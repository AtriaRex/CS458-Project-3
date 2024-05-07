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
- Open an internet browser and navigate to http://127.0.0.1:5000/login

# How to test
- Run the Flask app
- While the Flask app is running, start the test \
    ``` python -m pytest ```

# Important Notes
- 'Sign in with Google' feature works if and only if the host is set to 127.0.0.1 since there is no valid SSL certificate.
- See users.json file to see the pre-defined user credentials.
- You may set the host to your IPv4 address to be able to connect to the application using different devices that are connected to the same router.
