# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os
import json
# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen
from datetime import datetime
from datetime import timedelta
from multiprocessing import Process

story_genre = ''

def genre_text_generation(genre):
    
    if genre == 'political':
        file_dest = 'model/political'
        
    if genre == 'entertainment':
        file_dest = 'model/entertainment'
        
    if genre == 'crime':
        file_dest = 'model/crime'
        
    if genre == 'comedy':
        file_dest = 'model/comedy'
        
    if genre == 'worldnews':
        file_dest = 'model/worldnews'
        
    if genre == 'impact':
        file_dest = 'model/impact'
        
    return file_dest

# load up a model from memory. Note you may not need all of these options.

#ai = aitextgen(model_folder = 'model/action_files', to_gpu=False)
# ai = aitextgen(model_folder="model/", tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)
#ai = aitextgen(model="distilgpt2", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)




@app.route(f'{base_url}')
def home():
    return render_template('writer_home.html', generated=None)


@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


def get_article():
    os.system('bash GENERATEARTICLE.sh')
    notification = "done"
    data = session['data']
    return render_template('Write-your-story-with-AI.html', generated=data, notification="done")

@app.route(f'{base_url}/results/')
def results():
    if 'article' in session and 'data' in session:
        data = session['data']
        article = session['article']
        return render_template('Write-your-story-with-AI.html', generated=data, generated_article=article)
    elif 'data' in session and 'article' not in session:
        data = session['data']
        return render_template('Write-your-story-with-AI.html', generated=data)
    elif 'article' in session and 'data' not in session:
        article = session['article']
        return render_template('Write-your-story-with-AI.html', generated=None, generated_article=article)
    else:
        return render_template('Write-your-story-with-AI.html', generated=None, generated_article=None)


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """
#     print(os.getcwd())
    inputJson = open('/projects/4774738e-c466-40ea-9836-5c223b9a3ce2/TEMPLATE_WEBSITE/app/model/grover/input.json','a')
#     .spli()
    #THIS PART DOES THE HEADLINE GENERATION
    prompt = " ".join([word.capitalize() for word in request.form['prompt'].lower().split(" ")])
    print(prompt)
    genre_type = request.form['genre']
    print('genre type is: ', genre_type)
    story_genre = genre_text_generation(genre_type)
    print('file destination is: ', story_genre)
    ai = aitextgen(model_folder = story_genre, to_gpu=False)
    
#     if prompt is not None:
#         generated = ai.generate(
#             n=1,
#             batch_size=1,
#             prompt=str(prompt),
#             max_length=24,
#             temperature=1.0,
#             return_as_list=True
#         )
    
#     if prompt is not None:
#         generated = ai.generate(
#             n=1,
#             batch_size=1,
#             prompt=str(prompt),
#             temperature=1.0,
#             return_as_list=True
#         )
    generated = ai.generate_one(prompt=str(prompt), temperature = 1.0).split("\n")[0]
#     generated = str(generated[0])
    publishDate = datetime.today().strftime('%m-%d-%Y')
    writtenHeadline = generated #[0]
#     if '\n' in writtenHeadline:
#         writtenHeadline = writtenHeadline.replace('\n','')
    writedata = '{"title":"'+ writtenHeadline +'","text":"","summary":"","authors":"Updated","publish_date":"' + str(publishDate)+'","status":"success","url":"","domain":"","split":"gen"}'
    inputJson.truncate(0)
    inputJson.write(writedata)
    print(generated)
    print(type(generated))

    #TODO: write the variable 'generated' into the input.json for grover


    
    
#     #GENERATING ARTICLE
#     os.system('bash GENERATEARTICLE.sh')
    
    
    
#     return(jsonGarbage.get('"gens_article'))
    data = {'generated_ls': generated}
    session['data'] = generated
    return redirect(url_for('results'))
    

# async def async_get_data():
#     await os.system('bash GENERATEARTICLE.sh')
#     outputJson = open('/projects/4774738e-c466-40ea-9836-5c223b9a3ce2/TEMPLATE_WEBSITE/app/model/grover/output.json')
    
#     generated_article = outputJson.read()
# #     generated_articleList = json.loads(outputJson).get('gens_article')
# #     generated_article = generated_articleList[0].replace("\n"," ")
#     generated_article = generated_article.replace('"text": "", "summary": "", "authors": "Updated", "publish_date": "07-13-2022", "status": "success", "url": "", "domain": "", "split": "gen", ', "")
#     generated_article = generated_article.replace('"top_ps": [0.949999988079071],', "")
#     return generated_article
    
# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

@app.route(f'{base_url}/results/', methods=["POST"])
def generate_article():
    """
    view function that will return json response for generated text. 
    """
    #SUPPOSE WE HAVE THE CONTENT READY IN THE OUTPUT.JSON
    #RENDERING THIS INTO session[data] so that we can fill the content onto the homepage
#     os.system('bash GENERATEARTICLE.sh')
    data = session['data']
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=get_article,
        daemon=True
    )
    heavy_process.start()
#     return redirect(url_for('results'))
    return render_template('Write-your-story-with-AI.html', generated=data, notification="processing")
#     return render_template('Write-your-story-with-AI.html', generated=data)



@app.route(f'{base_url}/show_article/', methods=["POST"])
def show_article():
    """
    view function that will return json response for generated text. 
    """
    #SUPPOSE WE HAVE THE CONTENT READY IN THE OUTPUT.JSON
    #RENDERING THIS INTO session[data] so that we can fill the content onto the homepage
    outputJson = open('/projects/4774738e-c466-40ea-9836-5c223b9a3ce2/TEMPLATE_WEBSITE/app/model/grover/output.json','r')
#     data = session['data']
    try:
        jsonStuff = outputJson.read()
        generated_articleList = json.loads(jsonStuff)["gens_article"]
        generated_article = generated_articleList[0].replace("\n"," ")
#     generated_article = generated_article.replace('"text": "", "summary": "", "authors": "Updated", "publish_date": "07-13-2022", "status": "success", "url": "", "domain": "", "split": "gen", ', "")
#     generated_article = generated_article.replace('"top_ps": [0.949999988079071],', "")
#     generated_article = await async_get_data()
    except json.decoder.JSONDecodeError:
        return render_template('Write-your-story-with-AI.html', notification = "processing",generation_status="not finished yet")
     
                                
    
    #i think i can try
    
    print(generated_article.encode("ascii","ignore").decode())
    data = {'generated_article': generated_article.encode("ascii","ignore").decode()}
    session['article'] = generated_article
    return redirect(url_for('results'))

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc11.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
