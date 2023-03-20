from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/predict_tr',methods=['GET','POST'])
def predict_tr():
    user = request.form['user']

    response = jsonify({
        'player' : util.get_player(user),
        'actual_TR': util.get_actual_TR(),
        'predicted_TR':util.get_predicted_TR(user)
    })
    response.headers.add('Access-Control-Allow-Origin','*')

    return response

if __name__ == "__main__":
    util.load_saved_artifacts()
    print("Starting Python Flash Server for Tetra League TR Prediction...")
    app.run()