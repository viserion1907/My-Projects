""" LifeServe Blood Institute (lBI) blood-group program """

import sys
import matplotlib as plt
from hospital import check_demand
from datetime import date

# File constants
DONORS_FILE = 'donors.txt'
BAGS_FILE = 'bags.txt'
DONORS_NEW_FILE = 'donors-new.txt'
BAGS_NEW_FILE = 'bags-new.txt'
# Menu choices
CHECK_INVENTORY = 1
ATTEND_BLOOD_DEMAND = 2
RECORD_NEW_DONATION = 3
STOCK_VISUAL_REPORT = 4
EXIT = 5


def create_dictionary():
    """ Create a blood-group transfusion compatibility table in the form of a dictionary """
    blood_compatibility = {'O-': ['O-'],
                           'O+': ['0-', 'O+'],
                           'B-': ['O-', 'B-'],
                           'B+': ['O-', 'O+', 'B-', 'B+'],
                           'A-': ['O-', 'A-'],
                           'A+': ['O-', 'O+', 'A-', 'A+'],
                           'AB-': ['O-', 'B-', 'A-', 'AB-'],
                           'AB+': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+']}
    return blood_compatibility


def load_db(donor_fname, stock_fname):
    """ This function takes in two file names as parameters, reads both files and stores their data in a dictionary """
    donor_dict = {}  # Create an empty donor dictionary
    try:
        donor_file = open(donor_fname, 'r')
        for each_donor in donor_file:
            each_donor = each_donor.strip().split(',')  # Remove leading and trailing characters and split
            # Get each field individually
            donor_id = int(each_donor[0])
            name = each_donor[1]
            phone = each_donor[2]
            email = each_donor[3]
            blood_group = each_donor[4]
            last_donation_date = each_donor[5]
            # Append data to dictionary
            donor_dict[donor_id] = [name, phone, email, blood_group, last_donation_date]
        donor_file.close()

    except FileNotFoundError:
        sys.exit('No such file or directory')

    except IOError:
        sys.exit('Some error in the file I/O occurred')

    except:  # Generic handler to capture any other unspecified error
        sys.exit('Something went wrong')

    stock_dict = {}  # Create an empty stock dictionary
    try:
        stock_file = open(stock_fname, 'r')
        for each_bag in stock_file:
            each_bag = each_bag.strip().split(',')
            bag_id = int(each_bag[0])
            blood_group = each_bag[1]
            date_collected = each_bag[2]
            # Append data to dictionary
            stock_dict[bag_id] = [blood_group, date_collected]
        stock_file.close()

    except FileNotFoundError:
        sys.exit('No such file or directory')

    except IOError:
        sys.exit('Some error in the file I/O occurred')

    except:  # Generic handler to capture any other unspecified error
        sys.exit('Something went wrong')

    return donor_dict, stock_dict


def save_db(donor_fname, stock_fname):
    """ This function updates the donor and bags files, and saves them into new files """
    donors, stock = load_db(DONORS_FILE, BAGS_FILE)  # Call the load_db() function
    donor_fname = DONORS_NEW_FILE
    donor_dict_new = {}
    donor_file = open(donor_fname, 'w')
    for each_donor in range(1,100):
        # each_donor = each_donor.strip().split(',')  # Remove leading and trailing characters and split
        # Get each field individually
        # donor_id = int(each_donor[0])
        # name = each_donor[1]
        # phone = each_donor[2]
        # email = each_donor[3]
        # blood_group = each_donor[4]
        # last_donation_date = each_donor[5]
        # Append data to dictionary
        # donor_dict_new[donor_id] = [name, phone, email, blood_group, last_donation_date]
        print(each_donor)
    donor_file.write(str(DONORS_NEW_FILE))

    donor_file.close()

    bags_file = open(stock_fname, 'w')
    bags_file.close()

    return donor_dict_new


def main():
    """ This function starts running the main program plus other related functions """
    print(check_demand())
    print('<<< LifeServe Blood Institute >>>\n')
    print('Loading database...')
    print('Enter the database file names without .txt extension\nor just press Enter to accept defaults')
    donors_db = input('Donors database (donors): ').lower()  # Convert filename to lowercase letters
    if len(donors_db) == 0:  # If input field is left blank, use default values
        donors_db = DONORS_FILE
    else:
        # Concatenate filename with extension so that user does not have to enter it and strip to remove extra
        # spaces
        donors_db = donors_db.strip() + '.txt'
    stock_db = input('Stock inventory database (bags): ').lower()
    if len(stock_db) == 0:
        stock_db = BAGS_FILE
    else:
        stock_db = stock_db.strip() + '.txt'

    if load_db(donors_db, stock_db):  # Ensure that the files are loaded successfully
        print('Database loaded successfully\n')

        choice = 0  # Hold the user's menu choice
        while choice != EXIT:
            # Display the menu
            display_menu()

            choice = int(input('Enter your choice: '))  # Get the user's choice
            print()
            if choice == CHECK_INVENTORY:
                check_inventory()
            elif choice == ATTEND_BLOOD_DEMAND:
                print('Currently', check_demand(), 'is required:', )
                print('Checking the stock inventory...')
            elif choice == RECORD_NEW_DONATION:
                print('Record new donation')
            elif choice == STOCK_VISUAL_REPORT:
                print('Stock visual report')
            elif choice == EXIT:
                print('Have a good day.')
            else:
                print('Invalid choice! Please try again.')


def display_menu():
    """ This function displays the menu """
    print('------------')
    print('Main Menu')
    print('------------')
    print('(1) Check inventory')
    print('(2) Attend to blood demand')
    print('(3) Record new donation')
    print('(4) Stock visual report')
    print('(5) Exit')


def check_inventory():
    """ This function searches for any bags older than 30 days, and if found, it displays their ID numbers so that staff
     can dispose them of them """
    donors, stock = load_db(DONORS_FILE, BAGS_FILE)  # Call the load_db() function
    print('Following bags are out of their use-by date')
    for key, value in donors.items():
        # Return last donation date corresponding to a date string in the format YYYY-MM-DD
        last_donation_dt = date.fromisoformat(value[-1])
        today = date.today()  # Set today's date
        bag_age = (today - last_donation_dt).days  # Calculate difference in number of days
        donors[key] += [str(bag_age)]  # Add a new field for days old to the dictionary and convert it to string
        # print(last_donation_dt.isoformat())  # Represent date object in ISO
        bag_age = int(value[-1])  # Convert the age of the bag value to integer
        if bag_age > 30:  # Search for any bags older than 30 days
            print(key)  # Display the ID
    donors_update, stock_update = save_db(DONORS_FILE, BAGS_FILE)
    print('Please dispose of them. Press any key when done...\nUpdated database files saved to disk.\n')


# main()

# print(create_dictionary())
save_db(DONORS_NEW_FILE, BAGS_NEW_FILE)
