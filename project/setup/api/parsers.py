from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(
    name='page',
    type=int,
    location='args',
    required=False,
    help='Выберите страницу'
)

status_parser: RequestParser = RequestParser()
status_parser.add_argument(
    name='status',
    type=str,
    location='args',
    required=False,
    help='При указании в поле значения "new" выведет свежие фильмы по году'
)
