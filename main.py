
from flask import Flask,request,jsonify,render_template
from flask_ngrok import run_with_ngrok
from transformers import pipeline

USE_GPU = True  # set true if using gpu runtime

if USE_GPU:
    summarizer = pipeline("summarization",device=0)
else:
    summarizer = pipeline("summarization")

app = Flask(__name__)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
run_with_ngrok(app)   
#change if need
DEFAULT_MAX = 150
DEFAULT_MIN = 10
  
@app.route("/")
def home():
    # return "<h1> Test summarizer api </h1>"
    return render_template('index.html')

@app.route("/help")
def help():
  return jsonify(
      {
          
      '/summary':{
          'POST options':{
              'text':'the text to be summarized',
                'min':'minimum lenght the summarized text should be (optional) default:'+str(DEFAULT_MIN),
                'max':'maximum lenght the summarized text should be (optional) default:'+str(DEFAULT_MAX)
                },
                 
          'returns':{
              'full_text':'the text you sent to summarize',
                'min':'minimum lenght  of the summarized text that you sent',
                'max':'maximum lenght  of the summarized text that you sent',
                'summary':'summarized text'
                }

                  }
       })

@app.route('/summary', methods=['POST']) 
def summary(): 
  if request.method == 'POST': 

    # print (request.is_json)
    content = request.get_json()
    # print (content)
    if 'full_text' in  content:
        text = content.get('full_text')
    else:
      return jsonify({'error': 'need text parameter','for_help':request.host_url+'help'})

    if 'min' in content:
        min_length = int(content.get('min'))
    else:
        min_length = DEFAULT_MIN

    if 'max' in content:
        max_length = int(content.get('max'))
    else:
        max_length = DEFAULT_MAX

    summarized = summarizer(text, min_length=min_length, max_length=max_length)
    # return jsonify(content)

    return jsonify({
                    'full_text': text,
                    'min_lenght':min_length,
                    'max_length':max_length, 
                    'summary': summarized
                    })
    
app.run()

# get host from down ends with .ngrok.io
# endpoints{
#  /summary: post_params [text,max,min]  retruns [full_text,min_length,max_length]
#   /help: returns endpoints
#  }
# use postman for testing
# 🥱🥱