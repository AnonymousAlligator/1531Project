Auth Functions

Auth_login:
-When a user registers, they are automatically logged in at the end of registration (since they are given a token).

-When a user is logged in but a login attempt is made once again with same credentials, the system will get an error but the user will remain logged in.

########################################
Channel Functions

channel_leave:
-If all users leave a certain channel, that channel will be deleted from the Flockr.

-If an owner leaves the channel and they are the only owner, they will receive an error prompting them to make another user a memeber of the channel.


channel_join:
-Creating a channel will automatically add the user as a member of the channel.

channel_addowner:
- If the user being added is not a member of the channel, an error will be given. 

channel_removeowner:
- If the caller of the function is removing themself and they are the only member of the channel, they will receive an error prompting them to add someone else to the channel.

- If the caller of the function is the only owner, they will receive an error prompting them to add someone else as owner first. 

channels_list:
-If a user isn't a part of any channels, the channel list is empty.

channels_create:

-Channels ID's are asssigned in the order that channel_create is called. 

-Multiple channels in a single Flockr can't have the same name.

-When a channel is created by a user, they are immediately a member and owner of that channel.

######################################
Messages Functions

message_send:
-If multiple people in a channel send messages at the same time, the messages are sent in order of increasing u_ID.

message_remove:
-After a message is sent, the message can be deleted at any point in time in the future (no time limit to delete it).

message_edit:
-After a message is sent, the message can be edited at any point in time in the future (no time limit to edit it).

##########################################
User Functions

user_profile_setname:

-Any character string as long as between 3 and 50 will be accepted.

-Special Characters will be allowed in first name and last name fields.

-Both name fields accepts uppercase and lowercase letters.

user_profile_sethandle:
-Handle can't contain spaces,newlines or tabs.

-Handle can contain special characters

-Handle can accept both uppercase and lowercase characters.



######################################################
search:

-Search string isn't case sensitive (will search for 'hello' as well if 'Hello' is the search string).

-If no input is received, no search results are returned (can't run the search on empty space)

-No limit on how many search results returned

-Deleted messages will not be returned in the search results.

