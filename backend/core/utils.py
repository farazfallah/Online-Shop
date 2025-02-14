from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, TokenError

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        access_token = auth_header.split(' ')[1]
    else:
        access_token = request.COOKIES.get('access_token')

    if not access_token:
        raise AuthenticationFailed('توکن دسترسی یافت نشد')
    
    try:
        access_token_obj = AccessToken(access_token)
        user_id = access_token_obj.payload.get('user_id')
        return user_id
    except TokenError:
        raise AuthenticationFailed('توکن نامعتبر است یا منقضی شده است')