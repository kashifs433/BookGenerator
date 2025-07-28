import random
import string

class BoookIDGenerator:
    @staticmethod
    def generate_id():
        characters = string.ascii_letters + string.digits
        BookID = ''.join(random.choice(characters) for _ in range(10))
        return BookID
