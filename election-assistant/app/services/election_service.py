import json
import os
from datetime import datetime, date
from config import Config

class ElectionService:
    """Service for managing election data"""

    def __init__(self):
        self.elections_dir = Config.ELECTIONS_DIR

    def get_election(self, election_id):
        """Load election data by ID"""
        file_path = os.path.join(self.elections_dir, f"{election_id}.json")
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def get_default_election(self):
        """Get the default/current election"""
        return self.get_election(Config.DEFAULT_ELECTION)

    def get_all_elections(self):
        """Get list of all available elections"""
        elections = []
        if not os.path.exists(self.elections_dir):
            return elections

        for filename in os.listdir(self.elections_dir):
            if filename.endswith('.json'):
                election_id = filename[:-5]
                election = self.get_election(election_id)
                if election:
                    elections.append(election)

        return sorted(elections, key=lambda x: x['election_date'], reverse=True)

    def get_current_phase(self, election):
        """Determine which phase of the election we're currently in"""
        today = date.today().isoformat()

        for phase in election['phases']:
            if phase['start_date'] <= today <= phase['end_date']:
                return phase

        return None

    def get_upcoming_events(self, election, limit=5):
        """Get upcoming key dates"""
        today = date.today().isoformat()
        upcoming = [
            event for event in election['key_dates']
            if event['date'] >= today
        ]
        return sorted(upcoming, key=lambda x: x['date'])[:limit]

    def days_until_event(self, event_date):
        """Calculate days until an event"""
        if isinstance(event_date, str):
            event_date = datetime.fromisoformat(event_date).date()

        today = date.today()
        delta = event_date - today
        return delta.days

    def days_until_election(self, election):
        """Calculate days until election day"""
        return self.days_until_event(election['election_date'])
