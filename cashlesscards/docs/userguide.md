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

### Create and edit customer accounts 



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
