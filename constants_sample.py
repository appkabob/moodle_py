#
# ---
# --- MOODLE CONSTANTS --- #
# ---
#

MOODLE_QUERY_URL = 'http://YOUR_MOODLE_DOMAIN/webservice/rest/server.php'
WSTOKEN = 'YOUR_WS_TOKEN'  # see README for instructions on where to find this
MOODLEWSRESTFORMAT = 'json'

MOODLE_HEADERS = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }

# Moodle also sometimes calls SCO IDs cmid or Course Module ID.
# These are specific activities you want to be able to check on,
# for example when calling core_course_get_course_module to check
# completion status. You can document them here so you don't have
# to keep looking for them, and your code will also be more readable.
# Recommend replacing "SPECIFIC_SCORM_MODULE" with the actual name
# of the activity.
SCO_IDS = {
    'SPECIFIC_SCORM_MODULE': 12,
    'SPECIFIC_LABEL': 46
}

# Document the IDs of all your Moodle courses so you don't have to keep
# hunting them down. Change "course1", "course2", etc. to the names of
# specific courses in your system.
COURSE_IDS = {
    'course1': 3,
    'course2': 4,
    'course3': 6,
    'course4': 7
}

# Used to send test messages when you're testing out the messaging
# functionality so you can see what it would look like before sending
# messages to real users. You can find any user's ID by going to their
# profile page and looking in the URL:
# http://YOUR_MOODLE_DOMAIN/user/profile.php?id=2
ADMIN_USER_ID = 2

# Listing the email addresses of specific admin users can help take those
# out of grade reports.
MOODLE_ADMIN_USERS = ['user1@example.com',
                      'user2@example.com',
                      'user3@example.com'
                      ]
