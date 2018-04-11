from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def routeDate():
  if(request.user_agent.browser):
    return render_template('salah.html')
  else:
    return "Hore Benar, link selanjutnya : \n"


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 80))
  app.run(host='0.0.0.0', port=port)