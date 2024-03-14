from fastapi import FastAPI, status, Request, Header
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from functools import wraps
from typing_extensions import Annotated
from main.utilities.utils import get_hash_of_password
