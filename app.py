#importing flask and all dependencies..
from flask import Flask,redirect,url_for,render_template,request    
import os
import tensorflow as tf
from tensorflow import keras
from string import printable
from keras.preprocessing import sequence   
## WSGI Application
#app name-object declaration
app=Flask(__name__) 
      
# Recreate the exact same model, including its weights and the optimizer
new_model = tf.keras.models.load_model('model.h5')
# Show the model architecture
new_model.summary()
#decorator== parameters-rule(URL),options
@app.route('/')            
def home():
    ##return render_template('index.html')
    return 'This is my second API call!'

@app.route('/predict',methods=['POST'])            
def predict():
    #input_url= request.form.get("url")
    url = request.get_json() 
    print(url)
    # #test_malicious = 'wordsmith.org/words/pignus.html'
    url1 = url
    # Step 1: Convert raw URL string in list of lists where characters that are contained in "printable" are stored encoded as integer 
    url_int_tokens = [[printable.index(x) + 1 for x in url1 if x in printable]]
    # Step 2: Cut URL string at max_len or pad with zeros if shorter
    max_len=75
    X = sequence.pad_sequences(url_int_tokens, maxlen=max_len)
    target_proba = new_model.predict(X, batch_size=1)
    def print_result(proba):
        if proba > 0.5:
            return "malicious"
        else:
            return "benign"
        result=print_result(target_proba[0])
    return print_result(target_proba[0]) 
    
##starting point of program      
if __name__=="__main__":    
     app.run(port=3000, debug=True)    