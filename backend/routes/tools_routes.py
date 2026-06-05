# from flask import Blueprint, render_template

# tools_bp = Blueprint('tools', __name__)

# @tools_bp.route('/tools')
# def tools():
#     return render_template('tools.html')

from flask import Blueprint, render_template
from routes.home_routes import get_user_data

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/tools')
def tools():
    user_name, user_level, user_domain = get_user_data()

    return render_template(
        'tools.html',
        user_name=user_name,
        user_level=user_level,
        user_domain=user_domain
    )