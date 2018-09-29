# Cashless cards system

Congratulations on choosing Cashless cards as your internal transaction  
system. Its a clean, lightweight web application designed to provide a 
cashless service in a "closed" environment, such as offices, clinics, and 
schools, using NFC capable ID cards or an otherwise unique customer number. 

## Set up



## Permissions

The system limits certain functionality based on a user's permissions. These 
can be assigned at the individual user level or at group. We strongly 
recommend working at the group level as we've found it much easier to manage 
this way. 

The permissions used by cashless cards are: 
- Create and edit vouchers
- Create and edit customer accounts
- Conduct transactions
- Assign vouchers to customers
- Can view transaction log

### Create abd edit vouchers

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



### Assign vouchers to customers



### Can view transaction log



## Search

This is the main entry point into the cashless cards system. Place the cursor 
into the search box and use a USB card scanner to scan a NFC smart ID card. 
This will write the decimal card number into the search box. You can then 
click the search button to find that customer's account. 

On navigating to the account, the system will check if the customer is 
eligible for any vouchers. It will reset their voucher balance if it hasn't 
already done so within the application period. 

If no one is logged into the system (or you're logged in but have no 
permissions), all you'll be able to see is the customer's name, cash balance, 
voucher balance, and total balance. This can be useful if you want to provide 
a terminal for customer's to check their own details. 

If you have permission to conduct transactions, two buttons will also appear 
on this view. These take you to forms that allow you to credit and debit the 
customer's account respectively. 


## Customers



## Vouchers



## Transactions



## Activity log
