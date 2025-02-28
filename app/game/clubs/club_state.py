class ClubState:
    def __init__(self):
        self.active_event = None
        self.played_matches = 0
        self.club_status = 'idle'
        self.problem = None
        self.req_list = []
        self.error_count = 0

    def reset_game_state(self):
        self.__init__()  # Reset to initial state

    def set_active_event(self, event):
        self.active_event = event

    def add_played_match(self):
        self.played_matches += 1

    def set_club_status(self, status):
        self.club_status = status

    def set_problem(self, problem):
        self.problem = problem

    def reset_problem(self):
        self.problem = None

    def set_req_list(self, req_list):
        self.req_list = req_list

    def add_error_count(self):
        self.error_count += 1

    def reset_error_count(self):
        self.error_count = 0
