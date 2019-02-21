


class InstagramApiError(Exception):
    pass

class CheckpointRequired(InstagramApiError):
    pass
    

class ChallengeRequired(InstagramApiError):
    pass
    

class ConsentRequired(InstagramApiError):
    pass

class LoginRequired(InstagramApiError):
    pass
    
class FeedbackRequired(InstagramApiError):
    pass
    
    
class AccountDisabled(InstagramApiError):
    pass    
    
    
class HeadersTooLarge(InstagramApiError):
    pass
    

class IncorrectPassword(InstagramApiError):
    pass
    
    
class IncorrectPassword(InstagramApiError):
    pass
    

class InvalidSmsCode(InstagramApiError):
    pass
    

class SentryBlock(InstagramApiError):
    pass
    

class InvalidUser(InstagramApiError):
    pass
        

class ForcedPasswordReset(InstagramApiError):
    pass

class EmptyResponse(InstagramApiError):
    pass
    
exceptions = {name: exc for name, exc in dict(**locals()).items() \
    if not name.startswith('_')}
