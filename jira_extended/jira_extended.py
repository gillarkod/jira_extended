"""
Module that extends jira with additional functionality
"""
import requests
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


def copy_board(self, board_id):
    """
    Copy an existing board
    """
    url = self._get_url(
        'rapidview/{}/copy'.format(board_id),
        base='{server}/rest/greenhopper/1.0/{path}',
    )
    response = self._session.put(
        url,
    )

    raw_issue_json = response.json()
    return Board(self._options, self._session, raw=raw_issue_json)

jira.JIRA.copy_board = copy_board


@property
def board_name(self):
    """
    Get the name of the board
    """
    return self.raw.get('name')


@board_name.setter
def board_name(self, name):
    """
    Set the name of the board
    """
    url = self._get_url(
        'rapidviewconfig/name',
    )
    self._session.put(
        url,
        data=json.dumps(
            {
                'id': self.id,
                'name': name,
            }
        ),
    )

jira.resources.Board.name = board_name


@property
def board_admins():
    """
    Dummy function to enable the setter
    """
    pass


@board_admins.setter
def board_admins(self, admins):
    """
    Set the admins of the board
    """
    url = self._get_url(
        'rapidviewconfig/boardadmins',
    )
    self._session.put(
        url,
        data=json.dumps(
            {
                'id': self.id,
                'boardAdmins': admins,
            }
        ),
    )

jira.resources.Board.admins = board_admins


@property
def board_filter():
    """
    Dummy function to enable the setter
    """
    pass


@board_filter.setter
def board_filter(self, filter_id):
    """
    Set the filter of the board
    """
    url = self._get_url(
        'rapidviewconfig/filter',
    )
    self._session.put(
        url,
        data=json.dumps(
            {
                'id': self.id,
                'savedFilterId': filter_id,
            }
        ),
    )

jira.resources.Board.filter = board_filter


def share_filter(self, jira_filter, share):
    """
    Set the shares for a filter
    """
    username, password = self._session.auth
    session = requests.Session()
    session.post(
        url='{}/login.jsp'.format(self._options['server']),
        data={
            'os_username': username,
            'os_password': password,
            'login': 'Log In',
        }
    )
    session.post(
        url='{}/secure/EditFilter.jspa'.format(self._options['server']),
        data={
            'filterId': jira_filter.id,
            'filterName': jira_filter.name,
            'shareValues': share,
            'atl_token': session.cookies.get('atlassian.xsrf.token'),
            'Save': 'Save',
            'filterDescription': None,
            'favourite': None,
            'groupShare': None,
            'projectShare': None,
            'roleShare': None,
            'returnUrl': None,
        }
    )

jira.JIRA.share_filter = share_filter
