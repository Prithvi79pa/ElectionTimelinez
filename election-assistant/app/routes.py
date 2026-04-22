from flask import Blueprint, render_template, jsonify, request
from app.services.election_service import ElectionService
from app.services.state_service import StateService
from app.services.timeline_service import TimelineService
import json
import os
from config import Config

bp = Blueprint('main', __name__)

election_service = ElectionService()
state_service = StateService()
timeline_service = TimelineService()

@bp.route('/')
def index():
    """Home page"""
    election = election_service.get_default_election()
    states = state_service.get_all_states()
    return render_template('index.html', election=election, states=states)

@bp.route('/timeline')
def timeline():
    """Timeline view"""
    state_code = request.args.get('state')
    election_id = request.args.get('election')

    timeline_data = timeline_service.get_personalized_timeline(
        state_code=state_code,
        election_id=election_id
    )

    states = state_service.get_all_states()

    return render_template('timeline.html',
                         timeline=timeline_data,
                         states=states,
                         selected_state=state_code)

@bp.route('/guide')
def guide():
    """Step-by-step process guide"""
    state_code = request.args.get('state')

    # Load registration process
    process_file = os.path.join(Config.CONTENT_DIR, 'registration_process.json')
    with open(process_file, 'r') as f:
        process_data = json.load(f)

    state = state_service.get_state(state_code) if state_code else None
    states = state_service.get_all_states()

    return render_template('process-guide.html',
                         process=process_data,
                         state=state,
                         states=states,
                         selected_state=state_code)

@bp.route('/faq')
def faq():
    """FAQ page"""
    faq_file = os.path.join(Config.CONTENT_DIR, 'faqs.json')
    with open(faq_file, 'r') as f:
        faq_data = json.load(f)

    return render_template('faq.html', faq=faq_data)

@bp.route('/resources')
def resources():
    """Resource directory"""
    state_code = request.args.get('state')
    state = state_service.get_state(state_code) if state_code else None
    states = state_service.get_all_states()

    return render_template('resources.html',
                         state=state,
                         states=states,
                         selected_state=state_code)

# API endpoints for dynamic interactions

@bp.route('/api/timeline')
def api_timeline():
    """API endpoint for timeline data"""
    state_code = request.args.get('state')
    election_id = request.args.get('election')

    timeline_data = timeline_service.get_personalized_timeline(
        state_code=state_code,
        election_id=election_id
    )

    return jsonify(timeline_data)

@bp.route('/api/progress')
def api_progress():
    """API endpoint for progress checklist"""
    state_code = request.args.get('state')
    completed = request.args.get('completed', '').split(',') if request.args.get('completed') else []

    checklist = timeline_service.get_progress_checklist(
        state_code=state_code,
        completed_steps=completed
    )

    return jsonify(checklist)

@bp.route('/api/state/<state_code>')
def api_state(state_code):
    """API endpoint for state data"""
    state = state_service.get_state(state_code)
    if not state:
        return jsonify({'error': 'State not found'}), 404
    return jsonify(state)
