from models.course import BeyondComplianceCourse

print('\n\t1: Generate Reports for Beyond Compliance: Application Dissemination and Course Evaluation Reports')
print('\t2: Send Email to Beyond Compliance Users: "You should sign up for imminent live chat" email\n')
menu = input('Please enter a number corresponding to one of the options above:\n')

if menu == '1':

    print('\nGenerating reports...\n')
    BeyondComplianceCourse().generate_aa_reports()
    print('\nDone - you can find the reports in this project\'s "output" directory')

elif menu == '2':

    print('Gathering recipients...')
    course = BeyondComplianceCourse()
    users_to_email = course.get_enrolled_users_not_registered_for_live_chat()

    is_test = True
    if is_test:
        print('Dev mode: if you answer yes, message(s) will be sent, but they\'ll go to the admin user instead of would-be recipient(s). Proceed? y/n:')
    else:
        print('If you answer yes to the following this will email actual users. Proceed? y/n:')
    send_emails = input()

    if send_emails.lower() == 'y' or send_emails.lower() == 'yes':
        course.send_email_you_should_register_for_live_chat('March 30 at 1 pm', '60', users_to_email, is_test)
        print('Done')
    else:
        print('Canceled, nothing sent')

else:
    print('Error: you must enter a number corresponding to one of the menu options')
