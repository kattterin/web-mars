import flask
from flask import jsonify, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [i.to_dict(rules=('-jobs', '-departments.user'))
                 for i in users]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=["GET"])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    print(1)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(
                rules=('-jobs', '-departments.user'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'email', 'surname', 'age', 'position', 'speciality', 'address',
                  'password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        name=request.json['name'],
        email=request.json['email'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address']
    )
    user.set_password(request.json['password'])

    if 'id' in request.json:
        if db_sess.query(User).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
        user.id = request.json['id']

    elif 'modified_date' in request.json.keys():
        user.modified_date = request.json['modified_date']

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=["POST"])
def edit_one_jobs(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    if 'name' in request.json.keys():
        user.name = request.json['name']
    if 'email' in request.json.keys():
        user.email = request.json['email']
    if 'surname' in request.json.keys():
        user.surname = request.json['surname']
    if 'age' in request.json.keys():
        user.age = request.json['age']
    if 'position' in request.json.keys():
        user.position = request.json['position']
    if 'speciality' in request.json.keys():
        user.speciality = request.json['speciality']
    if 'address' in request.json.keys():
        user.address = request.json['address']
    if 'modified_date' in request.json.keys():
        user.modified_date = request.json['modified_date']

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
