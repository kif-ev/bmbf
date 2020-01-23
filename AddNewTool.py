import config
import random
import string
import databaseConnect
from pprint import pprint

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    if (config.debug):
        pprint(lettersAndDigits)
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

if __name__ == "__main__":
    token = randomStringDigits(150)
    if config.debug:
        pprint(token)
    databaseConnect.InsertTokenToDB(token)
    pprint("Created Token: " + token)
