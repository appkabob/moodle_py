# Pre-Requisites:

Tested with Moodle 3.2.2+

You will need to do some setup in your Moodle installation to enable API calls to be made.

1. Create a Custom Service, where you can define what Functions (API calls) the user is allowed to make
2. Create a Moodle user specifically for API access
3. Add the user as an Authorized user to the Custom Service

Then go back and allow access to some additional Functions.

# Detailed Instructions for the above Pre-Requisites

1. Site administration > Plugins > Web services > External services
    1. Click "Add"
    2. Enter a name and short name. I named this the same as the project I was creating, so that if I have multiple projects needing access, I could create multiple tokens to give them only the access they need.
    3. Check "Enabled" and "Authorized users only"
    4. Click "Add Service"
2. Site administration > Users > Accounts > Add a new user
3. Site administration > Plugins > Web services > Manage tokens
    1. Click "Add"
    2. On the Service dropdown, select the service you created in Step 1
    3. Save changes

You probably also want to check the box next to Web services documentation.
* Site administration > Plugins > Web services > Manage protocols

That will enable you to access a page with a list of all the API calls you can make, their arguments, and the expected response.
You'll be able to access that page under:
* Site administration > Plugins > Web services > API Documentation