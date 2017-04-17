import json
import requests
import sys
import getopt

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)
USERNAME = 'clydei'
PASSWORD = '87119515987d9684281d9dc81771a3fcc1a70c7d'


# The repository to add this issue to
REPO_OWNER = 'clydei'
REPO_NAME = 'toad'

def make_github_issue(session, url, title, body=None, assignees=None, milestone=None, labels=None):
    '''Create an issue on github.com using the given parameters.'''

    # Create our issue
    issue = {'title': title,
             'body': body,
             'assignees': assignees,
             'milestone': milestone,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print 'Successfully created Issue "%s"' % title
    else:
        print 'Could not create Issue "%s"' % title
        print 'Response:', r.content
def usage():
    print '%s -f JSON_file_name -l label' % sys.argv[0]

def authorize():
    client_id = '896045b6a6f318e694cb'
    client_secret = '7eaa8b9ae31117a8ef7f12780871277a962373f4'


    authorization_base_url = 'https://github.ibm.com/login/oauth/authorize'
    token_url = 'https://github.ibm.com/login/oauth/access_token'
    #token_url = 'https://github.ibm.com/oauth2/token'

    #from oauthlib.oauth2 import BackendApplicationClient
    #client = BackendApplicationClient(client_id=client_id)
    from requests_oauthlib import OAuth2Session
    github = OAuth2Session(client_id=client_id)
    #token = github.fetch_token(token_url, client_id=client_id, client_secret=client_secret)

 # Redirect user to GitHub for authorization
    authorization_url, state = github.authorization_url(authorization_base_url)
    print 'Please go here and authorize,', authorization_url

 # Get the authorization verifier code from the callback url
    redirect_response = raw_input('Paste the full redirect URL here:')

 # Fetch the access token
    github.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)


    return github

def main(argv):
    DATAFILE = 'c:\A1OpenTech\issue.json'
    try:
        opts, args = getopt.getopt(argv, "hf:l:", ["help", "file=", "--label="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ('-f', "--file"):
            DATAFILE = arg
        elif opt in ('-l', "--label"):
            LABEL = arg


    with open(DATAFILE) as data_file:
        data = json.load(data_file)
        print(json.dumps(data))

    # Our url to create issues via POST
    url = '%s/%s/%s/issues' % (data['apiurl'],data['org'], data['repo'])
    # Create an authenticated session to create the issue
    session = requests.session()
    session.auth=(data['username'], data['token'])
    #session = authorize()

    for issue in data['issues']:
        make_github_issue(session, url, issue['title'], issue['body'], issue['assignees'], issue['milestone'], [LABEL])

if __name__ == "__main__":
    main(sys.argv[1:])
