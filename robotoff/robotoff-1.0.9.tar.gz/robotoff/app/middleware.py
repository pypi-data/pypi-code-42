from robotoff.models import db


class DBConnectionMiddleware:
    def process_resource(self, req, resp, resource, params):
        db.connect()

    def process_response(self, req, resp, resource, req_succeeded):
        if not db.is_closed():
            db.close()
