import os

# App Initialization
from . import create_app  # from __init__ file
# from .migrate import *

app = create_app(os.getenv("CONFIG_MODE"))


# Hello World!
@app.route('/')
def hello():
    return "Hello World!"

from .migrate import *


if __name__ == "__main__":
    app.run()
