from flask import render_template,url_for,jsonify,flash,redirect,request
from flask_login import current_user
from API import app
import pyperclip

# copy text to clipboard
@app.route("/api/copy-to-clipboard/<TEXT>")
def to_clipboard(TEXT):
	pyperclip.copy(TEXT)
	# return redirect(request.args.get('previous'))
	return redirect(url_for('manage_account',username=current_user.username)+"#v-pills-UserKey")