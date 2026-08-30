from django.contrib.auth.decorators import user_passes_test


def is_author(user):
    return user.groups.filter(name='Authors').exists()


author_required = user_passes_test(
    is_author,
    login_url='accounts:login'
)