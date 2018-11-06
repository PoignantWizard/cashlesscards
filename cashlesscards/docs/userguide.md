# Cashless cards system

Congratulations on choosing "Cashless cards" as your internal transaction  
system. Its a clean, lightweight web application designed to provide a 
cashless service in a "closed" environment, such as offices, clinics, and 
schools, using NFC capable ID cards or an otherwise unique customer number. 

## Set up

We recommend copying the cashlesscards project folder to an ubuntu server for 
best results. It can also run from other linux or windows machines, however 
we've not tested as thoroughly on these. As such, we haven't developed an 
automated deployment programme for these. If you wish to run from a windows 
machine or non-debian based linux machine, please see the Django documentation 
for deploying on your environment. 

The easiest way to set up and begin using the system on a debian based linux 
machine is to run deploy.py. You can do this by navigating to the cashlesscards 
project folder and typing "python3 deploy.py" into the command line. This will 
walk you through the installation and setup of the necessary dependancies. Once 
complete, it will ask you whether you want to start the webserver. If you enter 
"y", then it will start and you can begin viewing and using the system. 

If this has been successful, visit the admin page to setup your permission 
groups and users. See the [permissions section](#Permissions) for more details. 

## Permissions

The system limits certain functionality based on a user's permissions. These 
can be assigned at the individual user level or at group using the system's 
[admin](#Admin) facility. We strongly recommend working at the group level as 
we've found it much easier to manage this way. 

The permissions used by cashless cards are: 
- Create and edit vouchers
- Create and edit customer accounts
- Conduct transactions
- Assign vouchers to customers
- Can view transaction log

### Create and edit vouchers

If you have this permission, then a menu will appear in the top navigation bar 
with options to create new and view existing vouchers. 

To create a new voucher, hover over the "Vouchers" menu button and click "Create 
new". The form has three options: 
1. Application - this sets how often a voucher is applied to a customer's account 
    The options available are: daily, weekly, monthly, and annually. Webmasters 
    can limit these choices by removing an option from the customsettings.py file. 
2. Name - each voucher must have a unique name. If a voucher with the same name 
    exists already, then the system won't allow you to create another. 
3. Value - set the value of the voucher. The currency is set by the default option 
    in the customsettings.py file. Note that whatever currency set here is used for 
    all calculations. Currently the system doesn't apply exchange rates to 
    transactions completed in different currencies. 

To view, edit and delete existing vouchers, hover over the "Vouchers" menu button 
and click "View existing". The page will display a list of vouchers ordered by 
their name. You can also see their value and application rate. Click on a voucher's 
name to view this voucher. Here you will see two buttons: "Update" and "Delete". 
Clicking these will take you to new pages that allow you to edit the voucher details 
or delete the voucher respectively. Changing or deleting a voucher will impact all 
customer's that have this voucher assigned to them. 

### Create and edit customer accounts 

If you have this permission a menu will appear in the top navigation bar with 
options to create new and view existing customers. 

To create a new customer account, hover over the "Customers" menu button and click 
"Create new". The form has four options:
1. First name - this sets the customer's first name. 
2. Surname - this sets the customer's last name. 
3. Card number - use a card reader to input the number of the smart ID card. This 
    is used by the system to find a customer's account and provide transactions. 
4. Opening balance - you can enter a starting cash balance for a customer here. 
    The default is set to zero. Any value above zero will be recorded in the 
    transaction log as this counts as a crediting transaction. 

To view, edit and delete existing customer accounts, hover over the "Customers" 
menu button and click "View existing". The page will display a list of customers 
ordered by their surname then first name. You can also see their card number, 
cash balance and voucher balance. Click on a customer's name to view their account. 
Here you will see up to five options (depending on your permissions): 
- "Add cash to account" - conduct a credit transaction 
- "Deduct cash from account" - conduct a debit transaction 
- "Update" - edit a customer's details 
- "Delete" - delete a customer's account. They must have a cash balance of zero
    else the system won't allow you to remove their account. 
- "Assign voucher" - assign new vouchers or unassign existing vouchers. It won't 
    let you assign more than one of the same voucher. 

### Conduct transactions 

If you have this permission then two buttons will appear when viewing a customer's 
account. These are: 
- "Add cash to account" - clicking this will take you to a form that enables you to 
    credit the customer's account. The value you input will be added to the 
    customer's overall "cash balance" and will be available for use as soon as you 
    press the "Submit" button. 
- "Deduct cash from account" - clicking this will take you to a form that enables 
    you to debit the customer's account. The value you input will be automatically 
    deducted from the customer's available voucher balance first, then from their 
    cash account if the debit is larger than the voucher balance alone. This 
    process occurs as soon as you press the "Submit" button. 

### Assign vouchers to customers

If you have this permission then an additional button will appear when viewing a 
customer's account. This is labelled "Assign voucher". Clicking this will take you 
to a form that enables you to assign a new voucher to the customer. If the customer 
already has that voucher assigned to them, then the form won't allow you to assign 
it again. 

The form will also list any assigned vouchers and their value. Next to each voucher 
there's a button labelled "Unassign". Clicking this opens a confirmation box and, if 
you select "Yes", remove it from the customer's account. Any voucher balance already 
claimed today will remain until deducted. 

### Can view transaction log

If you have this permission then a menu button will appear in the top navigation bar 
labelled "Activity log". Clicking this takes you to the transaction log page. This 
displays all the transactions that have occured in the last month. The fields 
included are: 
- Customer - displays the customer's name as surname, first name 
- Time - gives the date and time of the transaction 
- Type - shows whether the transaction was a credit or a debit 
- Cash value - shows how much of the customer's cash balance was affected 
- Voucher value - shows how much of the customer's voucher balance was affected 

The page also has a button labelled "Download CSV". Clicking this allows you to 
download a CSV file of the current transaction log. 

## Search

This is the main entry point into the cashless cards system. Place the cursor 
into the search box and use a USB card scanner to scan a NFC smart ID card. 
This will write the decimal card number into the search box. You can then 
click the search button to find that customer's account. 

On navigating to the account, the system will check if the customer is 
eligible for any vouchers. It will reset their voucher balance if it hasn't 
already done so within the application period. This action will be recorded in 
the transaction log. See the [activity log section](#Activity log) for more details. 

If no one is logged into the system (or you're logged in but have no 
permissions), all you'll be able to see is the customer's name, cash balance, 
voucher balance, and total balance. This can be useful if you want to provide 
a terminal for customer's to check their own details. 

If you have permission to conduct transactions, two buttons will also appear 
on this view. These take you to forms that allow you to credit and debit the 
customer's account respectively. Other buttons may also appear depending on 
your permissions. See the [permissions section](#Permissions). 

## Customers

Customer accounts can be managed by hovering over the "Customers" menu button 
and clicking on the relevant options. You'll require the "Create and edit 
customer accounts" permission to do this. See the 
[permissions section](#Permissions) for more details. 

To create a new customer account, hover over the "Customers" menu button and click 
"Create new". The form has four options:
1. First name - this sets the customer's first name. 
2. Surname - this sets the customer's last name. 
3. Card number - use a card reader to input the number of the smart ID card. This 
    is used by the system to find a customer's account and provide transactions. 
4. Opening balance - you can enter a starting cash balance for a customer here. 
    The default is set to zero. Any value above zero will be recorded in the 
    transaction log as this counts as a crediting transaction. 

To view, edit and delete existing customer accounts, hover over the "Customers" 
menu button and click "View existing". The page will display a list of customers 
ordered by their surname then first name. You can also see their card number, 
cash balance and voucher balance. Click on a customer's name to view their account. 
Here you will see up to five options (depending on your permissions): 
- "Add cash to account" - conduct a credit transaction 
- "Deduct cash from account" - conduct a debit transaction 
- "Update" - edit a customer's details 
- "Delete" - delete a customer's account. They must have a cash balance of zero
    else the system won't allow you to remove their account. 
- "Assign voucher" - assign new vouchers or unassign existing vouchers. It won't 
    let you assign more than one of the same voucher. 

## Vouchers

Vouchers can be managed by hovering over the "Vouchers" menu button and clicking 
the relevant options. You'll require the "Create and edit vouchers" permission 
to do this See the [permissions section](#Permissions) for more details. 

To create a new voucher, hover over the "Vouchers" menu button and click "Create 
new". The form has three options: 
1. Application - this sets how often a voucher is applied to a customer's account 
    The options available are: daily, weekly, monthly, and annually. Webmasters 
    can limit these choices by removing an option from the customsettings.py file. 
2. Name - each voucher must have a unique name. If a voucher with the same name 
    exists already, then the system won't allow you to create another. 
3. Value - set the value of the voucher. The currency is set by the default option 
    in the customsettings.py file. Note that whatever currency set here is used for 
    all calculations. Currently the system doesn't apply exchange rates to 
    transactions completed in different currencies. 

To view, edit and delete existing vouchers, hover over the "Vouchers" menu button 
and click "View existing". The page will display a list of vouchers ordered by 
their name. You can also see their value and application rate. Click on a voucher's 
name to view this voucher. Here you will see two buttons: "Update" and "Delete". 
Clicking these will take you to new pages that allow you to edit the voucher details 
or delete the voucher respectively. Changing or deleting a voucher will impact all 
customer's that have this voucher assigned to them. 

To assign or remove a voucher from a customer's account, navigate to the customer's 
account page and click "Assign voucher". You'll require the "Assign vouchers to 
customers" to do this. See the [permissions section](#Permissions) for more details. 

Clicking this button will take you to a form that enables you to assign a new voucher
to the customer. If the customer already has that voucher assigned to them, then the
form won't allow you to assign it again. 

The form will also list any assigned vouchers and their value. Next to each voucher 
there's a button labelled "Unassign". Clicking this opens a confirmation box and, if 
you select "Yes", remove it from the customer's account. Any voucher balance already 
claimed today will remain until deducted. 

When you search for a customer using the seach form (see the [search section](#Search) 
for details), the system will check if the customer is eligible for any vouchers. It will 
reset their voucher balance if it hasn't already done so within the application period. 
This action will be recorded in the transaction log. See the [activity log section](#Activity log) 
for more details. 

## Transactions

To conduct a transaction, navigate to a customer's account by either searching for 
them using their card (see the [search section](#Search) for more details) or going 
through the customer list (see the [Customers section](#Customers) for more details). 

If you have the "Conduct transactions" permission then two buttons will appear when 
viewing a customer's account. These are: 
- "Add cash to account" - clicking this will take you to a form that enables you to 
    credit the customer's account. The value you input will be added to the 
    customer's overall "cash balance" and will be available for use as soon as you 
    press the "Submit" button. 
- "Deduct cash from account" - clicking this will take you to a form that enables 
    you to debit the customer's account. The value you input will be automatically 
    deducted from the customer's available voucher balance first, then from their 
    cash account if the debit is larger than the voucher balance alone. This 
    process occurs as soon as you press the "Submit" button. 

Both of these types of transactions are recorded in the transaction log for accounting 
and monitoring, particularly the use of vouchers. See the [activity log section](#Activity log) 
for more details. 

## Activity log

If you have the "Can view transaction log" permission then a menu button will appear in 
the top navigation bar labelled "Activity log". Clicking this takes you to the 
transaction log page. This displays all the transactions that have occured in the last 
month. The fields included are: 
- Customer - displays the customer's name as surname, first name 
- Time - gives the date and time of the transaction 
- Type - shows whether the transaction was a credit or a debit 
- Cash value - shows how much of the customer's cash balance was affected 
- Voucher value - shows how much of the customer's voucher balance was affected 

The page also has a button labelled "Download CSV". Clicking this allows you to 
download a CSV file of the current transaction log. 

## Admin

If you're a superuser, then you'll be able to access the system's admin facility. 
Click the "Admin" menu button to find it. This is split into two main sections: 
1. Authentication and Authorization
2. Cashless

### Authentication and Authorization
This section allows you to create, edit and remove users and permisssion groups. 
We strongly recommend working at the group level for assigning persmissions as 
we've found it much easier to manage this way. For more information, see the 
[permissions section](#Permissions). 

User accounts can then be assigned to a group and will inherit the group's 
permissions. They can be easily removed from a group if they no longer require 
those permissions. If the permissions are changed at group level then all members 
of that group will have their permissions changed to relect this automatically. 

### Cashless

This section allows you to see the data held about customers, their accounts and 
vouchers. You're also able to edit data here, which is useful for correcting any 
issues that may occur during use of the system. 

Note that any restrictions enforced by the main site's forms will not be enforced 
here so you risk introducing strange or incompatible data. We strongly recommend 
using the site's forms for any record creation or modification. Any adjustments to 
cash and voucher balances on a customer's account will also not be recorded in the 
transaction log, which may cause issues with any reporting or monitoring that you do. 
