"""
Module that extends jira with additional functionality
"""
import jira
from jira import JIRA


def move(self, project=None):
    """
    Move an issue to a project
    """
    response = self._session.get(
        '{}/move/{}/{}'.format(
            self._options.get('extended_url'),
            self.key,
            project,
        ),
        auth=self._session.auth
    )
    return response.text

jira.Issue.move = move
