import flask
import shell
app = flask.Flask(__name__)

@app.route('/')
def return_json_data():
    result = shell.compute_system_ocl_for_server()
    result = [[float(j) for j in i] for i in result]
    response = flask.jsonify({"vector":result})
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

if __name__== '__main__':
    app.run()