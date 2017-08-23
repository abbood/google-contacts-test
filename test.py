import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage

def PrintAllContacts(gd_client):
  feed = gd_client.GetContacts()
  for i, entry in enumerate(feed.entry):
    print '\n%s %s' % (i+1, entry.name.full_name.text)
    if entry.content:
      print '    %s' % (entry.content.text)
    # Display the primary email address for the contact.
    for email in entry.email:
      if email.primary and email.primary == 'true':
        print '    %s' % (email.address)
    # Show the contact groups that this contact is a member of.
    for group in entry.group_membership_info:
      print '    Member of group: %s' % (group.href)
    # Display extended properties.
    for extended_property in entry.extended_property:
      if extended_property.value:
        value = extended_property.value
      else:
        value = extended_property.GetXmlBlob()
      print '    Extended Property - %s: %s' % (extended_property.name, value)

def main():
# ...
    SCOPE = 'http://www.google.com/m8/feeds/contacts/'
    admin_email="abdullah@lobolabshq.com"

    flow = flow_from_clientsecrets(
        filename='client_secret.json',
        scope=SCOPE,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob',
        message='Please create a project in the Google Developer Console and place the client_secret.json '
                'authorization file along this script',
        login_hint=admin_email
    )

    storage = Storage('credentials.json')
    credentials = storage.get()
    if credentials is None:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args([]))
    # GData with access token
    token = gdata.gauth.OAuth2Token(
        client_id=flow.client_id,
        client_secret=flow.client_secret,
        scope=SCOPE,
        user_agent=flow.user_agent,
        access_token=credentials.access_token,
        refresh_token=credentials.refresh_token)

    gd_client = gdata.contacts.client.ContactsClient(domain="lobolabshq.com", auth_token = token)
    token.authorize(gd_client)

    PrintAllContacts(gd_client)
	


if __name__ == '__main__':
    main()
