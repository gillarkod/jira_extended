from jira_extended import JIRA

jira = JIRA(
    '<url>',
    basic_auth=(
        '<user>',
        '<password>',
    ),
    options={
        'extended_url': '<url>',
    }
)
jira.search_issues('project = "PROJECT1"')[0].move('PROJECT2')
