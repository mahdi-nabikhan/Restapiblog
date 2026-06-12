from rest_framework.throttling import UserRateThrottle

class LoginThrottle(UserRateThrottle):
    scope = "login"
    
    
    
class RegisterThrottle(UserRateThrottle):
    scope = 'register'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None
        return self.get_ident(request=request)
