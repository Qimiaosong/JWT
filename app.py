from flask import Flask, jsonify, request, make_response
import jwt, datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ElonMusk'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            #必须加上算法类型token才有效
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # print("ddddddd", data)
        except:
            return jsonify({'message': 'Token is invalid !'}), 403
        return f(*args, **kwargs)
    return decorated


@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is only available for people with valid tokens.'})


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == '666666':
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm=" Login Required"'})


if __name__ == "__main__":
    app.run(debug=True)
