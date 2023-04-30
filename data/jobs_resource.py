from datetime import datetime

from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource

from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators')
parser.add_argument('start_date', type=datetime)
parser.add_argument('is_finished', type=bool)
parser.add_argument('end_date', type=datetime)


# format="%Y-%m-%dT%H:%M"


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': jobs.to_dict(
            rules=('-user.jobs', '-team_leader.jobs', '-team_leader.departments', '-user.departments'))})

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            rules=('-user.jobs', '-team_leader.jobs', '-team_leader.departments', '-user.departments')) for item in
            jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            job=args['job'],
            team_leader=args['team_leader'],
            work_size=args['work_size']
        )

        if args['collaborators']:
            job.collaborators = args['collaborators']
        elif args['start_date']:
            job.start_date = args['start_date']

        elif args['end_date']:
            job.end_date = args['end_date']

        elif args['is_finished']:
            job.is_finished = args['is_finished']

        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_jobs_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"Job {jobs_id} not found")
