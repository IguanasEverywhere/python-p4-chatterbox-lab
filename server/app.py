from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()

    if request.method == 'GET':
        all_messages = []
        for message in messages:
            all_messages.append(message.to_dict())

        response = make_response(all_messages, 200)
        return response
    elif request.method == 'POST':
        data = request.json
        username = data.get('username')
        body = data.get('body')

        new_post = Message(username=username, body=body)

        db.session.add(new_post)
        db.session.commit()

        new_post_dict = new_post.to_dict()
        response = make_response(new_post_dict, 201)
        return response



@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if request.method == 'PATCH':
        data = request.json
        print('REQUEST.JSON', data)
        print('REQUEST.FORM', request.form) # This is empty! Even though it looks like it came from a form??
        for attr in data:
            setattr(message, attr, data.get(attr))
        # setattr(message, 'created_at', message.created_at)
        print(message.updated_at)
        db.session.add(message)
        db.session.commit()

        response = make_response(message.to_dict(), 200)
        return response

    if request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return make_response(message.to_dict(), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
