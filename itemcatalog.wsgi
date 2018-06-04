import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/")

from UdacityItemCatalog import app as application
application.secret_key = 'my_favourite_game'