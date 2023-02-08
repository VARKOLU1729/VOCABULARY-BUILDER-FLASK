from flask import Flask,render_template,url_for,redirect,request
import json
import requests
app = Flask(__name__)

@app.route("/hell")
def hell():
    return render_template('index.html')


@app.route("/well/<name>")   
def well(name):
    return f'''
    # <!DOCTYPE html>
    # <html style="background-color: #33475b">
    # <body>
    # <h1 style = 'color:White'>{name}</h1>
    # </body>
    # </html>
    # '''

@app.route("/Synonyms", methods = ['POST', 'GET'])   
def Synonyms():
    word = ''
    if request.method == 'POST':
        word = request.form['word']
        r = get_dictionary_response(word)
    return redirect(url_for('well',name = 'Synonyms of '+ word + " : " +r["synonyms"][0]))


@app.route("/Antonyms", methods = ['POST', 'GET'])
def Antonyms():
    word = ''
    if request.method == 'POST':
        word = request.form['word']
        r = get_dictionary_response(word)
    return redirect(url_for('well',name = 'Antonyms of '+ word + " : " +r["antonyms"][0]))


@app.route("/Definition", methods = ['POST', 'GET'])
def Definition():
    word = ''
    if request.method == 'POST':
        word = request.form['word']
        r = get_dictionary_response(word)
    return redirect(url_for('well',name = 'Definition of '+ word + " : " +r["meaning"]))


@app.route("/Sentence", methods = ['POST', 'GET'])
def Sentence():
    word = ''
    r = 0
    if request.method == 'POST':
        word = request.form['word']
        r = get_dictionary_response(word)
    return redirect(url_for('well',name = 'Example of '+ word + " : " +r["examples"]))

def get_dictionary_response(word):
    word_metadata = {}
    definition = "sorry, no definition is available."
    example = "sorry, no examples are available."
    synonyms = ["sorry, no synonyms are available."]
    antonyms = ["sorry, no antonyms are available."]
    # api_key = os.getenv("KEY_THESAURUS")
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key=b3b73004-8412-455e-a40a-2cfb3d87e9ee"
    response = requests.get(url)
    api_response = json.loads(response.text)
    if response.status_code == 200:
        for data in api_response:
            try:
                if data["meta"]["id"] == word:
                    try:
                        if len(data["meta"]["syns"]) != 0:
                            synonyms = data["meta"]["syns"][0]
                        if len(data["meta"]["ants"]) != 0:
                            antonyms = data["meta"]["ants"][0]
                        for results in data["def"][0]["sseq"][0][0][1]["dt"]:
                            if results[0] == "text":
                                definition = results[1]
                            if results[0] == "vis":
                                example = results[1][0]["t"].replace("{it}", "*").\
                                    replace("{/it}", "*")
                    except KeyError as e:
                        print(e)
            except TypeError as e:
                print(e)
            break
    word_metadata["meaning"] = definition
    word_metadata["examples"] = example
    word_metadata["antonyms"] = antonyms
    word_metadata["synonyms"] = synonyms
    return word_metadata


if __name__ == "__main__":
    app.run(port = '4000', debug = True)
