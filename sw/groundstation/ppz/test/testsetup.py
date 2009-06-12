import sys
import os.path

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(TEST_DIR, "..", ".."))

def get_messages():
    me = os.path.abspath(os.path.dirname(__file__))
    default = os.path.abspath(os.path.join(me, "..", "..", "..", "messages.xml"))
    return os.environ.get("MESSAGES_FILE", default)


