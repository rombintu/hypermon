from flask import Flask
from .nova.client import Nova

app = Flask(__name__)
admin_api = Nova()

from . import views