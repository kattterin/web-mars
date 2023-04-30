import flask
from flask import jsonify, request

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [i.to_dict(rules=('-user.jobs', '-team_leader.jobs', '-team_leader.departments', '-user.departments'))
                 for i in jobs]
        }
    )


@blueprint.route('/api/job/<int:job_id>', methods=["GET"])
def get_one_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': job.to_dict(
                rules=('-user.jobs', '-team_leader.jobs', '-team_leader.departments', '-user.departments'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'team_leader', 'work_size']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = Jobs(
        job=request.json['job'],
        team_leader=request.json['team_leader'],
        work_size=request.json['work_size']
    )
    if 'id' in request.json:
        if db_sess.query(Jobs).get(request.json['id']):
            return jsonify({'error': 'Id already exists'})
        job.id = request.json['id']

    if 'collaborators' in request.json.keys():
        job.collaborators = request.json['collaborators']
    elif 'start_date' in request.json.keys():
        job.start_date = request.json['start_date']

    elif 'end_date' in request.json.keys():
        job.end_date = request.json['end_date']

    elif 'is_finished' in request.json.keys():
        job.is_finished = request.json['is_finished']

    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/job/<int:job_id>', methods=["POST"])
def edit_one_jobs(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})

    if 'team_leader' in request.json.keys():
        job.team_leader = request.json['team_leader']
    if 'job' in request.json.keys():
        job.job = request.json['job']
    if 'collaborators' in request.json.keys():
        job.collaborators = request.json['collaborators']
    if 'work_size' in request.json.keys():
        job.work_size = request.json['work_size']
    if 'start_date' in request.json.keys():
        job.start_date = request.json['start_date']
    if 'end_date' in request.json.keys():
        job.end_date = request.json['end_date']
    if 'is_finished' in request.json.keys():
        job.is_finished = request.json['is_finished']

    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
