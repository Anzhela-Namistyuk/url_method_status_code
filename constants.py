from pathlib import Path

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Constant that we put in the dictionary value
# on ClientConnectorError instead status code
CONNECTION_ERROR_VALUE = -1

TEST_URL_1 = 'https://t.me/+9ZGvemKOKj4yNjdi'
TEST_WRONG_URL ='https://google'
TEST_INCORRECT_URL = 'https://google.coms'
