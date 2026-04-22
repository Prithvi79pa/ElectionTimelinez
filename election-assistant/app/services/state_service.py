import json
import os
from config import Config

class StateService:
    """Service for managing state-specific election rules"""

    def __init__(self):
        self.states_dir = Config.STATES_DIR
        self._states_cache = {}

    def get_state(self, state_code):
        """Load state data by code (e.g., 'CA', 'TX')"""
        state_code = state_code.upper()

        if state_code in self._states_cache:
            return self._states_cache[state_code]

        # Try exact match first
        file_path = os.path.join(self.states_dir, f"{state_code.lower()}.json")
        if not os.path.exists(file_path):
            # Try finding by state name
            state_data = self._find_state_by_name(state_code)
            if state_data:
                return state_data
            return None

        try:
            with open(file_path, 'r') as f:
                state_data = json.load(f)
                self._states_cache[state_code] = state_data
                return state_data
        except FileNotFoundError:
            return None

    def _find_state_by_name(self, state_name):
        """Find state by name (e.g., 'California')"""
        for filename in os.listdir(self.states_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.states_dir, filename)
                with open(file_path, 'r') as f:
                    state_data = json.load(f)
                    if state_data['state_name'].lower() == state_name.lower():
                        return state_data
        return None

    def get_all_states(self):
        """Get list of all available states"""
        states = []
        if not os.path.exists(self.states_dir):
            return states

        for filename in os.listdir(self.states_dir):
            if filename.endswith('.json'):
                state_code = filename[:-5].upper()
                state = self.get_state(state_code)
                if state:
                    states.append(state)

        return sorted(states, key=lambda x: x['state_name'])

    def get_state_deadline(self, state_code, deadline_type='registration_deadline'):
        """Get specific deadline from state's key_dates_override"""
        state = self.get_state(state_code)
        if not state:
            return None

        return state.get('key_dates_override', {}).get(deadline_type)

    def supports_online_registration(self, state_code):
        """Check if state supports online registration"""
        state = self.get_state(state_code)
        if not state:
            return False
        return state.get('online_registration', False)

    def supports_early_voting(self, state_code):
        """Check if state supports early voting"""
        state = self.get_state(state_code)
        if not state:
            return False
        return state.get('early_voting', False)

    def get_voter_id_requirements(self, state_code):
        """Get voter ID requirements for a state"""
        state = self.get_state(state_code)
        if not state:
            return None

        return {
            'required': state.get('voter_id_required', False),
            'accepted_types': state.get('accepted_id_types', [])
        }
