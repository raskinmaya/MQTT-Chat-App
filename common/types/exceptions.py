class UsernameAlreadyTaken(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username '{username}' is already taken.")

class UserNotFound(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"No record for username '{username}', user does not exist")