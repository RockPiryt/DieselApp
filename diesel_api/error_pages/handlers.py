#handlers.py

from flask import Blueprint, render_template

error_pages = Blueprint('error_pages', __name__)

@error_pages.app_errorhandler(404)#NOT FOUND
def error_404(error):
    return render_template('error_pages/404.html') , 404 


@error_pages.app_errorhandler(403)#FORBIDDEN ACCESS
def error_403(error):
    return render_template('error_pages/403.html') , 403 
