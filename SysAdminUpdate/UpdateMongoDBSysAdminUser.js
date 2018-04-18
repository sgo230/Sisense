// This script replaces the current Sisense web application Sys Admin user with another existing user
 
// Valid roles (friendly name in parentheses):
//     "admin" (administrator)
//     "contributor" (designer)
//     "dataAdmin" (data administrator)
//     "dataViewer" (data viewer)
 
var new_sys_admin_email = "sovenshinery@gmail.com" // Email address of new Sys. Admin user (user must already exist)
var current_sys_admin_new_role = "contributor" // New role for the current Sys. Admin user
 
use prismWebDB
 
var valid_users = []
db.users.find().forEach(function(row) {
    valid_users.push(row.email)
})
 
use prismConfig
 
var valid_roles = []
db.compiled_roles.find().forEach(function(row) {
    valid_roles.push(row.name)
})
 
if (!valid_roles.includes(current_sys_admin_new_role)) {
     
    print("Error: Invalid role name")
     
} else {
     
    if (!valid_users.includes(new_sys_admin_email)) {
         
        print("Error: Invalid user email address")
         
    } else {
         
        var super_id = db.compiled_roles.findOne({name: {$in: ["super"]}}, {_id: 1})["_id"].valueOf()
        var alt_id = db.compiled_roles.findOne({name: {$in: [current_sys_admin_new_role]}}, {_id: 1})["_id"].valueOf()
 
use prismWebDB
 
        current_super = db.users.find({"roleId": ObjectId(super_id)}, {"email": 1,"_id": 0}).toArray()[0]["email"]
         
        if (current_super == new_sys_admin_email) {
            print("Error: New Sys. Admin is identical to the current Sys. admin")
        } else {       
 
            db.users.updateOne(
                {"email": new_sys_admin_email},
                {$set: {"roleId": ObjectId(super_id)}}
                )
                 
            db.users.updateOne({
                "email": current_super},
                {$set: {"roleId": ObjectId(alt_id)}}
            )
        }   
    }
}