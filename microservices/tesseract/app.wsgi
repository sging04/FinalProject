import logging
import sys
import os 
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/Quizzle/FinalProject/microservices/tesseract')
from api import app as application
application.secret_key = os.urandom(32)
