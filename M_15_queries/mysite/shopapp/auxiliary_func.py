from django.contrib.auth.models import User
from django.http import Http404


def user_comparison(user: User, pk):
    if user.id != pk:
        try:
            owner = User.objects.get(id=pk)
        except User.DoesNotExist:
            raise Http404
    else:
        owner = user
    return owner