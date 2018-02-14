import random
import string


def generate_secret_key():
    characters = string.digits + string.ascii_letters + string.punctuation
    return ''.join([random.choice(characters) for i in range(50)])


SECRET_KEY = generate_secret_key()
