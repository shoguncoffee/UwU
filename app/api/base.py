from app.base import *

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query, Body
from app.__main__ import system
import app.src as src