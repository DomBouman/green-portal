from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('submissions', __name__)

@bp.route('/sessions/<int:session_id>/assignments/<int:assignment_id>/submissions/<int:submission_id>/update', methods=['GET', 'POST'])
@login_required
def enter_grade(session_id, assignment_id, submission_id):
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':
            grade = request.form.get('grade')

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                UPDATE submissions
                SET points_earned = %s
                WHERE id = %s;
            """,
            (grade, submission_id))

            con.commit()

            cur.execute("""
                SELECT submissions.content, submissions.points_earned, assignments.total_points FROM submissions
                JOIN assignments ON submissions.assignment_id = assignments.id
                WHERE submissions.id = %s;
            """,
            (submission_id,))

            submission = cur.fetchone()

            cur.close()
            con.close()

            return render_template('grade_submission.html', submission=submission)
        else:
            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                SELECT submissions.content, submissions.points_earned, assignments.total_points FROM submissions
                JOIN assignments ON submissions.assignment_id = assignments.id
                WHERE submissions.id = %s;
            """,
            (submission_id,))

            submission = cur.fetchone()

            cur.close()
            con.close()

            return render_template('grade_submission.html', submission=submission)