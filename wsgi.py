from app import app
import os
from dotenv import load_dotenv

config_folder = os.path.expanduser('/home/bluser/config')  # adjust as appropriate
load_dotenv(os.path.join(config_folder, '.env'))

if __name__ == 'main':
    app.run()
