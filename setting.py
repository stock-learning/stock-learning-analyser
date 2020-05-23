# Author: Carlos Henrique Ponciano da Silva
from dotenv import load_dotenv
import os
load_dotenv()

def get_env(env):
    return os.getenv(env)