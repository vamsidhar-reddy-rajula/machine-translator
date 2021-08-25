
# from import PipeCustomOrdinalEncoder, transform_dataset, CustomKNNImputer, return_df
import joblib
from flask import Flask, request, jsonify, render_template, make_response, url_for
from flask_restful import Api, Resource
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import tensorflow as tf
from google_translate import get_google_translation
import urllib

import json

app = Flask(__name__)
api = Api(app)

model_2 = tf.keras.models.load_model(
    "./src/api/best_model/20210824-053923-model")  # trained model
# checkpoint_path = "./models/base_model_7/20210824-031856-cp-0015.ckpt"
# model_2.load_weights(checkpoint_path)

en_tokenizer = joblib.load(
    './src/api/best_model/20210824-053923-english_tokenizer')  # tokenize the sentence
# map from numbers to french
inv_map = joblib.load('./src/api/best_model/20210824-053923-inverse_map')


class translate(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        pred = {}
        pred['english_input'] = ""
        pred['foreign_translation'] = ""
        return make_response(render_template('index.html', pred=pred), 200, headers)

    def post(self):
        # json_data = request.get_json()
        headers = {'Content-Type': 'text/html'}
        json_data = request.form.to_dict(flat=False)

        json_data = {k: v for k, v in json_data.items()}

        sentence_to_predict = json_data["english_sentence"]

        tokenized_sentence = pad_sequences(en_tokenizer.texts_to_sequences(
            sentence_to_predict), padding='post', maxlen=40)

        y_predict = model_2.predict(tokenized_sentence)

        fr_prediction = ' '.join([inv_map[prediction] for prediction in np.argmax(
            y_predict[0], 1) if prediction != 0])
        pred = {}
        pred['english_input'] = sentence_to_predict[0]
        pred['foreign_translation'] = fr_prediction
        pred['google_translation'] = get_google_translation(
            urllib.parse.quote(fr_prediction))
        # return jsonify(pred)
        print(pred)
        return make_response(render_template('index.html', pred=pred), 200, headers)


api.add_resource(translate, '/')
# app.add_url_rule('/favicon.ico',
#                  redirect_to=url_for('static', filename='favicon.ico'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
