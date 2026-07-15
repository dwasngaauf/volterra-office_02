import os
import sys
import importlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

from mangum import Mangum

main_module = importlib.import_module("main")
handler = Mangum(main_module.app)
