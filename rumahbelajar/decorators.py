from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def group_required(group_names):
    def check_groups(user):
        return user.is_authenticated and (
            user.groups.filter(name__in=group_names).exists() or user.is_superuser
        )
    return user_passes_test(check_groups)
