# Boilerplate project for Flask

The goal of this project is to include basic configuration, test setup etc
that is common for most of the Flask projects

## Development

After creating virtualenv and activating it install the requirements:

    pip install requirements

To start development server export an environment variable:

    export FLASK_APP=manage.py

And optionally:

    export FLASK_DEBUG=true

After that run:

    flask run
