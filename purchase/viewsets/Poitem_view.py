import json
import os
import pandas as pd
import datetime
from pathlib import Path
from wsgiref.util import FileWrapper

from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse, FileResponse