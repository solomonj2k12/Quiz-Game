import os
from flask import Flask, render_template,redirect,request

from json_file import create_riddle_data

app = Flask(__name__)


@app.route('/')
def index():
   return render_template('index.html')
    
    
@app.route('/setup', methods=['GET'])
def setup():
 
 if request.method == 'GET':
  players = request.args.get('players')
  if players is None:
   return render_template('setup.html')
  else:
   return redirect ('/usernames/{}'.format(players))
   
   
@app.route('/usernames/<players>',methods=['POST', 'GET'])
def usernames(players):
 
 players = int(players)
 
 if request.method == 'POST':
  create_riddle_data(players)
  return redirect('/riddle')
 return render_template('usernames.html', players=players)
 
 
 
@app.route('/riddle')
def riddle():
 return render_template('riddle.html')
 
 
 
@app.route('/leaderboards')
def leaderboards():
 return render_template('leaderboards.html')
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)






