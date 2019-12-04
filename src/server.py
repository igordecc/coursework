import flask
import shell
import numpy
app = flask.Flask(__name__)

@app.route('/')
def return_json_data():
    result, Aij = shell.compute_system_ocl_for_server()
    result = [[float(j) for j in i] for i in result]
    print(Aij)
    print(result)
    response = flask.jsonify({"Aij": Aij.tolist(),"vector":result})
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

if __name__== '__main__':
    app.run()