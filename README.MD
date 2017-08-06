# Purpose

Use this library to pull data from your Moodle instance via the Moodle API.

You can use it in combination with libraries like [reportlab](https://pypi.python.org/pypi/reportlab) to automatically generate custom reports out of Moodle, or use it to schedule custom emails to go out based on specific events in Moodle, e.g. email all users who have completed a particular activity in Moodle, but have not completed a synchronous event in Adobe Connect, for example.

This Python library can help bridge the gap between Moodle and your other systems.

# Pre-Requisites:

Tested with Moodle 3.2.2+

You will need to do some setup in your Moodle installation to enable API calls to be made.

1. Create a Custom Service, where you can define what Functions (API calls) the user is allowed to make.
Don't worry, you can always add to this later (specific functions listed at the bottom of this document)
2. Create a Moodle user specifically for API access
3. Add the user as an Authorized user to the Custom Service
4. Download this library, enter your information into the constants_sample.py file, rename it to constants.py and place it in your project's root

# Detailed Instructions for the above Pre-Requisites

1. **Site administration > Plugins > Web services > External services**
    1. Click "Add"
    2. Enter a name and short name. I named this the same as the project I was creating,
    so that if I have multiple projects needing access, I could create multiple tokens to give them only the access they need.
    3. Check "Enabled" and "Authorized users only"
    4. Click "Add Service"
    5. You should then see your token. Paste that into this project's constants_sample.py, and rename the file to constants.py.
2. **Site administration > Users > Accounts > Add a new user**
3. **Site administration > Plugins > Web services > Manage tokens**
    1. Click "Add"
    2. On the Service dropdown, select the service you created in Step 1
    3. Save changes

You probably also want to check the box next to Web services documentation:

* **Site administration > Plugins > Web services > Manage protocols**

That will enable you to access a page with a list of all the API calls you can make,
their arguments, and the expected response. You'll be able to access that page under:

* **Site administration > Plugins > Web services > API Documentation**

In Step 1 if you're wondering which of the hundreds of Functions to enable,
here are the ones currently used by this library:

* core_completion_get_activities_completion_status
* core_enrol_get_enrolled_users
* core_group_get_course_groups
* core_group_get_group_members
* core_message_send_instant_messages
* core_user_get_users
* gradereport_user_get_grades_table
* mod_scorm_get_scorm_sco_tracks
