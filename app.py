import numpy as np
from flask import Flask, request, render_template
import pickle

from resources.utils import *
from fastai2.vision.widgets import *
from fastai2.imports import *

import os


cwd = os.getcwd()
path = cwd + '/model'

app = Flask(__name__)

learn_inf = load_learner('model\export.pkl')

