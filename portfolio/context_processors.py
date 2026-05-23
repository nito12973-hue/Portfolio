from .models import Profile


def profile_data(_request):
    profile = Profile.get_solo()
    return {"profile": profile}
