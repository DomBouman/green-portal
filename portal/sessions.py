from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('sessions', __name__)

@bp.route('/sessions')
@login_required
def sessions():
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT courses.name, courses.course_code, sessions.session_name, sessions.day, sessions.start_time, sessions.end_time FROM user_sessions
        JOIN sessions ON user_sessions.session_id = sessions.id
        JOIN courses ON courses.id = sessions.course_id
        WHERE user_sessions.user_id = %s;
    """,
    (g.user[0],))

    sessions_list = cur.fetchall()

    return render_template('sessions.html', sessions_list=sessions_list)

@bp.route('/sessions/add/<int:course_id>')
@login_required
def add_session(course_id):
    con = db.get_db()
    cur = con.cursor() 

    cur.execute("""
        INSERT INTO sessions (course_id, session_name, day, start_time, end_time)
        VALUES (%s, %s, %s, %s, %s)
    """,
    (course_id, 'A', 'M', '12:00:00', "1:00:00"))

    con.commit()

    cur.close()
    con.close()

    return redirect(url_for('courses.edit_courses', id=course_id))
    

