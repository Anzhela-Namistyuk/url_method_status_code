from pathlib import Path

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# Constant that we put in the dictionary value
# on ClientConnectorError instead status code
CONNECTION_ERROR_VALUE = -1

TEST_URL_1 = 'https://t.me/+9ZGvemKOKj4yNjdi'
TEST_WRONG_URL = 'https://google'
TEST_INCORRECT_URL = 'https://google.coms'
TEST_URL_2 = 'https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:%D0%9F%D0%BE%D0%B8%D1%81%D0%BA'
