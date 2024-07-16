from flask import Flask, render_template, request

#from chatbot import chatbot
import os
from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
# Creating ChatBot Instancep

chatbot = ChatBot(
    'Bridging database with natural language',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        {
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand. I am still learning.',
        'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
) 
 # Training with Personal Ques & Ans 
training_data_quesans = open('training_data/HEALTH.txt').read().splitlines()
training_data = training_data_quesans
print(training_data)
trainer = ListTrainer(chatbot)
trainer.train(training_data) 
# Training with English Corpus Data 
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
app = Flask(__name__)
app.static_folder = 'static'  
@app.route("/")
def home():
    return render_template("index.html")   
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')        
    query= "select * from movielist where Movies='" +userText+"'"
    query1 = "select distrinct t.name from( select distinct t.name from( select distinct m.*, g.Name as gname from MOVIE m)left join MOVIE_GENRE mg on mg.MOVIE_ID = m.ID left Join GENRE g on g.ID = mg.GENRE_ID )t"
    query4 = "left join MOVIE_MEMBERS mm on mm.MOVIE_ID = t.ID"
    query5 = "left join MEMBERS mem on mem.ID = mm.MEMBERS_ID where t.YEAR > 2022"
    query6 = "order by t.RATING desc )"
    # List of data entries
    data_entries = [query, query1, query4, query5,query6]
    # Concatenate the data entries with new lines
    formatted_data = '\n'.join(data_entries)
    print(formatted_data)
    da=str(formatted_data)
    result_data = {
        'message': f"{str(chatbot.get_response(userText))}",
        'additional_value': f"{da}"
    }
    #print(userText)    
    return jsonify(result=result_data)

