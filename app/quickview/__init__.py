from flask import  Blueprint

quickview = Blueprint('quickview',__name__)
from . import views,errors