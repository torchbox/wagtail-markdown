import random
import string

import dj_database_url


def generate_secret_key():
    characters = string.digits + string.ascii_letters + string.punctuation
    return "".join([random.choice(characters) for i in range(50)])


SECRET_KEY = generate_secret_key()

DATABASE_URL = dj_database_url.config()
