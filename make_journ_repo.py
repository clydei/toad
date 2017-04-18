import json
import requests
import sys
import getopt

# Authentication for user filing issue (must have read/write access to
# repository to add issue to)





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

def add_collabo(session, url, user, perm ):
    '''Add collaborators to the repo'''

    # Create the url
    collabo_url = '%s/%s' % ( url, user )

    # Create the parameter
    perms = {'permission': perm }
    # Add the collaborator to our repository
    r = session.put(collabo_url, json.dumps(perms))
    if r.status_code == 204:
        print 'Successfully added collaborator "%s"' % user
    else:
        print 'Could not add collaborator "%s"' % user
        print 'Response:', r.content

def make_milestone(session, url, milestone ):
    '''Create milestones in the repo'''

    # Add the milestone to our repository
    r = session.post(url, json.dumps(milestone))
    if r.status_code == 201:
        print 'Successfully created milestone "%s"' % milestone['title']
    else:
        print 'Could not create milestone "%s"' % milestone['title']
        print 'Response:', r.content

def usage():
    print '%s -f JSON_file_name -l label' % sys.argv[0]


def main(argv):
    DATAFILE = 'c:\A1OpenTech\issue.json' #Default value. Read from JSON file
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

    # URL to add collaborators
    collabo_url = '%s/%s/%s/collaborators' % (data['apiurl'],data['org'], data['repo'])

    # URL to create milestones
    milestone_url = '%s/%s/%s/milestones' % (data['apiurl'],data['org'], data['repo'])

    # Create an authenticated session to create the issue
    session = requests.session()
    session.auth=(data['username'], data['token'])

    for user in data["collabo"]:
      add_collabo(session, collabo_url, user['username'], user['permission'])

    for milestone in data["milestones"]:
      make_milestone(session, milestone_url, milestone)

    for issue in data['issues']:
        make_github_issue(session, url, issue['title'], issue['body'], issue['assignees'], issue['milestone'], [LABEL])

if __name__ == "__main__":
    main(sys.argv[1:])
