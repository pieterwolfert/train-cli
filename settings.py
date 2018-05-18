import sys

class Credentials:
    def __init__ (self):
        #password and user should be saved in separate files
        with open('password', 'r') as f:
            self.password = f.readline().rstrip()
        with open('user', 'r') as f:
            self.user = f.readline().rstrip()

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password
