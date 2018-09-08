import os
from flask import Flask, render_template, redirect, request, url_for

from json_file import dump_data, create_riddle_data, get_player_data, set_player_turn, set_previous_answer,  check_player_answer, adjust_score_and_lives,\
eliminate_zero_lives_user, all_users_eliminated, start_question, player_question, ask_question, get_scores
from gameplay import wipe_gamefiles,  game_end_text, get_end_text

app = Flask(__name__)

app.secret_key = 'some_secret'

'''
route functions
'''


@app.route('/')
def index():
    '''
    simple routing for my index.html page to be rendered
    '''
    return render_template('index.html')
 
 
@app.route('/setup', methods=['GET'])
def setup():
    """
    gets template for set.html page but also if user clicks 
    the continue button when no option is selected 
    they are redirected back to the setup page, so this will remove any errors
    """
    if request.method == 'GET':
        players = request.args.get('players')
    if players is None:
        return render_template('setup.html')
    else:
        return redirect('/usernames/{}'.format(players))
   
   
@app.route('/usernames/<players>', methods=['POST', 'GET'])
def usernames(players):
    '''
    this is the page where the user will input there usernames for the game, 
    once this is completed, the user is redirected to the game page, 
    this is loaded with all the correcr info given earlier

    '''
    players = int(players)
 
    if request.method == 'POST':
        create_riddle_data(players)
        return redirect('/riddle')
    return render_template('usernames.html', players=players)
 
   
@app.route('/leaderboards')
def leaderboards():
    '''
    this will render the leaderboard template with all the scores, 
    that are collected from the games played,
    this is done by using get_scores
    '''
    data = get_scores()
    return render_template("leaderboards.html", data=data)

'''
quiz game loop
'''
@app.route('/riddle', methods=['GET', 'POST'])
def riddle():
    wipe_gamefiles()
    riddle_data = get_player_data()
    '''
    this part is the main loop, which keeps the game flowing and the question coming,
    untill all users are eliminated
    '''
    if request.method == 'POST':
        set_player_turn()
        set_previous_answer()
        correct_check = check_player_answer()
        adjust_score_and_lives(correct_check)
        eliminate_zero_lives_user()
        
        '''
        if a player loses all their lives they are eliminated from the game and 
        no longer can play and a message is shown to show what has happened
        '''
       
        if eliminate_zero_lives_user:
           
   
            if not all_users_eliminated():
                player_question()
                ask_question()
            
        riddle_data = get_player_data()
        '''
        this else statment gets the game statred and only runs once which is at the start of the game
        '''
    else:
        start_question()
        riddle_data[0]["turn"] = True
        dump_data(riddle_data)
        player_question()
        ask_question()
        
        '''
        once all players are eliminated they are redirected to the leaderboards where they can see where they are in the table
        '''
    if all_users_eliminated():
        wipe_gamefiles(True)
        game_end_text()
        data = get_scores()
        end_text = get_end_text()
        return render_template('leaderboards.html' ,data=data,
                                game_end_text="".join(end_text["game over text"]))
        
    
    
    end_text = get_end_text()
    riddle_data = get_player_data()
    '''
    this piece of code re renders the riddle template after an answer has been submitted with the corect information
    '''
    return render_template("riddle.html", correct_text="".join(end_text["correct text"]),
    eliminated_text="".join(end_text["eliminated text"]),
    quizmaster_text="".join(end_text["quizmaster text"]),
    question_text="".join(end_text["question text"]),
    riddle_data=riddle_data)
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
