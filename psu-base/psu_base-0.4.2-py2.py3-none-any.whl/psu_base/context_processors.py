from psu_base.services import auth_service


def auth(request):
    auth_object = auth_service.get_auth_object()
    return {'auth': auth_object}
