import numpy as np
from flask import Flask, request, render_template
import pickle

from resources.utils import *
from fastai2.vision.widgets import *
from fastai2.imports import *

import os


cwd = os.getcwd()
path = Path()
Path().ls(file_exts='.pkl')

app = Flask(__name__)

model = load_learner(path/'model/export.pkl')



#Defining the home page for the web service
@app.route('/')
def home():
    return render_template('index.html')

#Writing api for inference using the loaded model
@app.route('/predict',methods=['POST'])

#Defining the predict method get input from the html page and to predict using the trained model

def predict():
    
        labels = ['grizzly','black','teddy']
        #Collecting values from the html form and converting into respective types as expected by the model

        file = request.files['file']

        if file:
            filename = file.filename
            file.save(os.path.join("resources/tmp", filename))

        #fastai predicts from a pandas series. so converting the list to a series
        #to_predict = "resources/bears/teddy/images586.jpg"
        to_predict = "resources/tmp/"+filename

        #Getting the prediction from the model and rounding the float into 2 decimal places
        prediction=model.predict(to_predict)

        #print("result: ",prediction[0])

        return render_template('index.html', prediction_text='Your Prediction :  {} '.format(prediction[0]))


if __name__ == "__main__":
    #predict()
    app.run(debug=True)