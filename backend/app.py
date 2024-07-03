import numpy as np
import smtplib

from PIL import Image
import pandas as pd


# import tensorflow as tf
# from tf.keras.models import load_model
# from tf.keras.preprocessing.image import load_img, img_to_array

import tensorflow  
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array


import json
from flask import Flask, render_template, request, send_file, redirect

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes




server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login("madalateja053@gmail.com", "rmtunamjbwnvgfvw")




# Load the model
model = load_model('./SkinDisease.h5')  

def predict_image(image_upload):
  im = Image.open(image_upload)
  im = im.resize((150, 150))    
  im_array = np.asarray(im)
  im_array = im_array / 255.0
  im_input = tf.reshape(im_array, shape = [1, 150, 150, 3])

  predict_array = model.predict(im_input)[0]

  df = pd.DataFrame(predict_array)
  df = df.rename({0:'Probability'}, axis = 'columns')
  prod = ['flea_allergy', 'hotspot', 'mange', 'ringworm']
  df['Animal'] = prod
  df = df[['Animal', 'Probability']]

  predict_label = np.argmax(model.predict(im_input))

  if predict_label == 0:
      predict_product = 'flea_allergy'
  elif predict_label == 1:
      predict_product = 'hotspot'
  elif predict_label == 2:
      predict_product = 'mange'
  else:
      predict_product = 'ringworm'

  return predict_product, df



# prediction_string,y= predict_image('./dog_test.jpeg')
# server.sendmail("sainithyamsani@gmail.com", "s6114187@gmail.com",  f'Hello, your dog is {prediction_string}! we will be arriving shortly to help you out!')



@app.route('/upload', methods=['POST'])
def upload():
    email = request.form['email']  # Get other form data
    image_file = request.files['image']  # Get the image file
    print(email)
    
    # Save the image to a desired location
    image_file.save('uploaded_image.jpg')
    prediction_string,y= predict_image('./dog_test.jpeg')
    server.sendmail("madalateja053@gmail.com", email,  f'Hello, your dog is {prediction_string}! we will be arriving shortly to help you out!')


@app.route('/')
def home():
    #  print('Hello, World!')
    return redirect('http://localhost:5501/caninecare/index.html')

if __name__ == '__main__':
    app.run(debug=True)
