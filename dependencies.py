""" Script to install all modules required by this project. """
import pip


def install(package):
    pip.main(['install', package])


if __name__ == '__main__':
    install('tweepy')
    install('flask')
    install('flask_socketio')
    install('eventlet')
    install('geocoder')
    install('requests')
    install('indicoio')
    install('sqlite3')
