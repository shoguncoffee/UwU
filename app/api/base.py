from app.base import *
import app.src as src

from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query, Body
from app.__main__ import system