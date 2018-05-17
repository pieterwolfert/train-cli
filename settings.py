import sys

class Credentials:
    def __init__ (self):
        #password and user should be saved in separate files
        self.password = open('password', 'r')
        self.password = self.password.readline().rstrip()
        self.user = open('user', 'r')
        self.user = self.user.readline().rstrip()

    def getUser(self):
        return self.user

    def getPassword(self):
        return self.password
