from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash,
    send_from_directory
)
from Project import db
main = Blueprint("main", __name__)
