from datetime import date, datetime, timedelta
from .election_service import ElectionService
from .state_service import StateService

class TimelineService:
    """Service for creating personalized election timelines"""

    def __init__(self):
        self.election_service = ElectionService()
        self.state_service = StateService()

    def get_personalized_timeline(self, state_code=None, election_id=None):
        """Generate a personalized timeline for a user"""
        election = self.election_service.get_election(election_id) if election_id else self.election_service.get_default_election()

        if not election:
            return None

        timeline = {
            'election': election,
            'events': [],
            'current_phase': None,
            'next_action': None,
            'days_until_election': self.election_service.days_until_election(election)
        }

        # Get state-specific data if provided
        state = self.state_service.get_state(state_code) if state_code else None

        # Build events list
        for event in election['key_dates']:
            event_data = event.copy()

            # Override with state-specific dates if available
            if state and event.get('state_specific'):
                state_date = self._get_state_specific_date(state, event)
                if state_date:
                    event_data['date'] = state_date
                    event_data['state_customized'] = True

            # Calculate days until event
            event_data['days_until'] = self.election_service.days_until_event(event_data['date'])
            event_data['is_past'] = event_data['days_until'] < 0
            event_data['is_today'] = event_data['days_until'] == 0
            event_data['is_urgent'] = 0 <= event_data['days_until'] <= 7

            timeline['events'].append(event_data)

        # Sort events by date
        timeline['events'].sort(key=lambda x: x['date'])

        # Determine current phase
        timeline['current_phase'] = self.election_service.get_current_phase(election)

        # Determine next action
        timeline['next_action'] = self._get_next_action(timeline['events'], state)

        # Add state information if provided
        if state:
            timeline['state'] = state

        return timeline

    def _get_state_specific_date(self, state, event):
        """Get state-specific date for an event"""
        if not state or not event.get('state_specific'):
            return None

        # Check for override in state data
        key_dates = state.get('key_dates_override', {})

        # Map event categories to state override keys
        category_map = {
            'registration': 'registration_deadline',
            'voting': 'early_voting_start',
            'absentee': 'mail_ballot_request_deadline'
        }

        override_key = category_map.get(event.get('category'))
        if override_key and override_key in key_dates:
            return key_dates[override_key]

        return None

    def _get_next_action(self, events, state=None):
        """Determine the next action the user should take"""
        today = date.today().isoformat()

        # Find the next upcoming event
        upcoming_events = [e for e in events if e['date'] >= today and not e['is_past']]

        if not upcoming_events:
            return {
                'action': 'Election has passed',
                'description': 'Check back for the next election',
                'priority': 'low'
            }

        next_event = upcoming_events[0]

        # Generate action based on event category
        if next_event['category'] == 'registration':
            if state and not state.get('online_registration'):
                return {
                    'action': 'Register to vote by mail or in person',
                    'description': f"Registration deadline is {next_event['date']}. Online registration is not available in {state['state_name']}.",
                    'priority': 'high' if next_event['is_urgent'] else 'medium',
                    'deadline': next_event['date'],
                    'days_remaining': next_event['days_until']
                }
            else:
                return {
                    'action': 'Register to vote online',
                    'description': f"Registration deadline is {next_event['date']}.",
                    'priority': 'high' if next_event['is_urgent'] else 'medium',
                    'deadline': next_event['date'],
                    'days_remaining': next_event['days_until']
                }

        elif next_event['category'] == 'absentee':
            return {
                'action': 'Request your absentee ballot',
                'description': f"Deadline to request mail-in ballot is {next_event['date']}.",
                'priority': 'high' if next_event['is_urgent'] else 'medium',
                'deadline': next_event['date'],
                'days_remaining': next_event['days_until']
            }

        elif next_event['category'] == 'voting':
            if 'Early Voting' in next_event['event']:
                return {
                    'action': 'Vote early',
                    'description': f"Early voting begins {next_event['date']}.",
                    'priority': 'medium',
                    'deadline': next_event['date'],
                    'days_remaining': next_event['days_until']
                }
            else:
                return {
                    'action': 'Vote on Election Day',
                    'description': f"Election Day is {next_event['date']}. Find your polling place and make a plan to vote.",
                    'priority': 'critical',
                    'deadline': next_event['date'],
                    'days_remaining': next_event['days_until']
                }

        return {
            'action': 'Stay informed',
            'description': 'Check for updates on the election process',
            'priority': 'low'
        }

    def get_progress_checklist(self, state_code=None, completed_steps=None):
        """Generate a checklist of steps to complete"""
        if completed_steps is None:
            completed_steps = []

        state = self.state_service.get_state(state_code) if state_code else None

        checklist = [
            {
                'id': 'check_eligibility',
                'title': 'Check eligibility to vote',
                'completed': 'check_eligibility' in completed_steps,
                'required': True
            },
            {
                'id': 'register_to_vote',
                'title': 'Register to vote',
                'completed': 'register_to_vote' in completed_steps,
                'required': True
            },
            {
                'id': 'verify_registration',
                'title': 'Verify voter registration',
                'completed': 'verify_registration' in completed_steps,
                'required': True
            },
            {
                'id': 'research_candidates',
                'title': 'Research candidates and issues',
                'completed': 'research_candidates' in completed_steps,
                'required': False
            },
            {
                'id': 'find_polling_place',
                'title': 'Find your polling place',
                'completed': 'find_polling_place' in completed_steps,
                'required': True
            },
            {
                'id': 'plan_to_vote',
                'title': 'Make a plan to vote',
                'completed': 'plan_to_vote' in completed_steps,
                'required': True
            },
            {
                'id': 'vote',
                'title': 'Cast your ballot',
                'completed': 'vote' in completed_steps,
                'required': True
            }
        ]

        # Add state-specific items
        if state:
            if state.get('voter_id_required'):
                checklist.insert(4, {
                    'id': 'prepare_id',
                    'title': f"Prepare required ID ({state['state_name']} requires photo ID)",
                    'completed': 'prepare_id' in completed_steps,
                    'required': True
                })

        total = len([item for item in checklist if item['required']])
        completed = len([item for item in checklist if item['required'] and item['completed']])

        return {
            'items': checklist,
            'total_required': total,
            'completed_required': completed,
            'progress_percentage': int((completed / total) * 100) if total > 0 else 0
        }
