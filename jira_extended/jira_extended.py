"""
Module that extends jira with additional functionality
"""
import jira
from jira import (
    JIRA,
    JIRAError,
)


def move(self, project=None):
    """
    Move an issue to a project
    """
    response = self._session.get(
        '{}/move/{}/{}?url={}'.format(
            self._options.get('extended_url'),
            self.key,
            project,
            self._options['server'],
        ),
        auth=self._session.auth
    )
    if response.status_code != 200:
        raise JIRAError(response.text)
    else:
        return True

jira.Issue.move = move
