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


def customfield_by_name(self, name):
    """
    Get the value of a customfield by name
    """
    # Get all fields from Jira. This is expensive, so only do it once
    if not hasattr(self, '_fields'):
        response = self._session.get(
            self._base_url.format(
                server=self._options['server'],
                rest_path=self._options['rest_path'],
                rest_api_version=self._options['rest_api_version'],
                path='field',
            ),
            auth=self._session.auth,
        )
        if response.status_code != 200:
            raise JIRAError(response.text)
        else:
            self._fields = response.json()

    for field in self._fields:
        if field.get('name') == name:
            break
    else:
        raise JIRAError('Could not find customfield')
    return getattr(self.fields, field.get('id'))

jira.Issue.customfield_by_name = customfield_by_name
