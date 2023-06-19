from typing import Optional

import flask

class Context:

    def get_user(self) -> 'UserAuthSchema':
        if hasattr(flask.g, 'current_user'):
            return flask.g.current_user
        return None

    def get_user_id(self) -> Optional[int]:
        return self.get_user().get('id')

