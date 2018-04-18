This MongoDB script lets customers directly edit the Sisense Repository to change the Sys. Admin user from one existing user to another.

Currently, Sisense customers cannot change the web application SysAdmin user through the UI or the REST API due to licensing errors related to having two SysAdmin users at once or not having a SysAdmin user.

This script directly manipulates MongoDB to update the SysAdmin from one user to another. Compatible with Sisense 6.7+ only.

The script takes two parameters:

<b>new_sys_admin_email</b> - Set this to the email address for the new SysAdmin user. The user must already exist in Sisense

<b>current_sys_admin_new_role</b> - Set this to the role the existing SysAdmin will have after the change

Run in Robo 3T or another graphical MongoDB client shell.
