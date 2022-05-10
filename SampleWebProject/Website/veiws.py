from flask import Blueprint, render_template, request,flash, redirect, url_for,jsonify
# Blueprint means define that this file is the blueprint of our application
from flask_login import login_required,  current_user
from .models import db,Note,User
import json
sampleviews = Blueprint('sampleviews', __name__)

@sampleviews.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if(len(note))<1:
            flash("Note is too short", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user)

@sampleviews.route('/delete-note',methods=['POST'])
def delete_note():
    note=json.loads(request.data)
    noteId=note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})