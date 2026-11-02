"""User-facing failure categories; never render API bodies, credentials, or tokens."""


def instagram_failure(error):
    name = type(error).__name__
    status = getattr(getattr(error, 'response', None), 'status_code', None)
    if status == 429 or name in {'ClientThrottledError', 'PleaseWaitFewMinutes'}:
        return 'Instagram rate-limited the request. Stop retries and wait; check the app for verification prompts.'
    if name in {'ChallengeRequired', 'ChallengeError', 'ChallengeUnknownStep', 'FeedbackRequired'}:
        return 'Instagram requires account review or verification. Resolve prompts in the official app before retrying.'
    if name in {'LoginRequired', 'ClientLoginRequired', 'BadPassword'} or status == 401:
        return 'Instagram rejected the session. Run full setup, preferably with username/password, and replace INSTA_SESSION.'
    if status == 403 or name == 'ClientForbiddenError':
        return ('Instagram refused the profile change (HTTP 403). A successful login check does not grant write access. '
                'Check the official app for restrictions and try changing your picture there manually. '
                'If you used a browser session, create a password-based session through full setup and replace INSTA_SESSION. '
                'A cloud-IP restriction is also possible; the exact cause is not confirmed. Do not repeatedly retry.')
    return ('Instagram did not confirm the profile update. Check the official app for restrictions or verification prompts. '
            'The cause is unknown; do not assume your password is wrong.')
