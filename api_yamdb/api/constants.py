MIN_SCORE_AMOUNT: int = 1
MAX_SCORE_AMOUNT: int = 10

NAME_MAX_LENGTH: int = 256
SLUG_MAX_LENGTH: int = 50
TITLE_NAME_MAX_LENGTH: int = 256
REVIEW_TEXT_MAX_LENGTH: int = 200
COMMENT_TEXT_MAX_LENGTH: int = 200

USER_ROLE_MAX_LENGTH: int = 50
USER_EMAIL_MAX_LENGTH: int = 254
USER_USERNAME_MAX_LENGTH: int = 150

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES: tuple[tuple[str, str], ...] = (
    ('user', 'USER',),
    ('moderator', 'MODERATOR'),
    ('admin', 'ADMIN'),
)