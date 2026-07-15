from mangum import Mangum
import os

os.chdir(os.path.dirname(os.path.dirname(__file__)))

from main import app
handler = Mangum(app)
