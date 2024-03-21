from flask import Flask, jsonify, render_template, request
import json
import preprocess_text
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    print("Prediction....")
    try:
        print("55555555")
        tf_idf = pickle.load(open('./Models/tfidf_tokenizer.pkl', 'rb'))
        rf_model = pickle.load(open('./Models/random_forest.pkl', 'rb'))
        tokenizer = pickle.load(open('./Models/tf_tokenizer.pkl', 'rb'))
        print("55555555")
        model = load_model('./Models/lstm.h5', compile=False)
        text = request.form['text']
        print("11111")
        new_text = preprocess_text.clean_text(text)
        print("22222")
        vec = tf_idf.transform([new_text])
        ml_pred = rf_model.predict(vec)
        ml_pred = int(ml_pred[0])
        print("Prediction....")
        new_text = preprocess_text.clean_text(text)
        sequence = tokenizer.texts_to_sequences([new_text])
        padded_sequence = pad_sequences(sequence, padding='post')
        dl_pred = model.predict(padded_sequence)
        dl = dl_pred[0][0]
        dl = int(dl > 0.5)
        print("PRED :",dl)
        return jsonify({"status": 200, "dl_pred": json.dumps(dl), "ml_pred": json.dumps(ml_pred)})
    except:
        print("Exception occured...")
        pass

    return jsonify({"status": 422, "message": "Internal Server Error"})


if __name__ == '__main__':
    app.run(debug=True)
