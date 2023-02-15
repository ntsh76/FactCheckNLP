import random

def model(claim, source):
    result = random.randint(0,1)
    confidence = random.uniform(.3,1)
    return result, confidence