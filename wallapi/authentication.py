from datetime import timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from rest_framework.authtoken.models import Token



class ExpiringTokenAuthentication(TokenAuthentication):
    '''
    Expiring token for mobile and desktop clients.
    It expires every 24hrs requiring client to supply valid username
    and password for new one to be created.
    '''
    def authenticate_credentials(self, key, request=None):
        token = Token.objects.select_related('user').filter(key=key).first()
        if token is None:
            raise AuthenticationFailed({'error': 'Invalid or Inactive Token', 'is_authenticated': False})

        if not token.user.is_active:
            raise AuthenticationFailed({'error': 'Invalid or innactive user', 'is_authenticated': False})

        now = timezone.now()
        expired_at = token.created + timedelta(days=1)
        if expired_at < now:
            
            raise AuthenticationFailed({
                'error': 'Token expired at ' + str(expired_at),
                'is_authenticated': False
            })
        return token.user, token


