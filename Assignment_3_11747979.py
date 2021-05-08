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

# Create a blood-group transfusion compatibility table in the form of a dictionary
blood_compatibility = {'O-': ['O-'],
                       'O+': ['0-', 'O+'],
                       'B-': ['O-', 'B-'],
                       'B+': ['O-', 'O+', 'B-', 'B+'],
                       'A-': ['O-', 'A-'],
                       'A+': ['O-', 'O+', 'A-', 'A+'],
                       'AB-': ['O-', 'B-', 'A-', 'AB-'],
                       'AB+': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+']}


def main():
    """ This function starts running the main program plus other related functions """
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
                print('Following bags are out of their use-by date')
                check_inventory()
                print('Please dispose of them. Press any key when done...\nUpdated database files saved to disk.\n')
            elif choice == ATTEND_BLOOD_DEMAND:
                demand = check_demand()
                if demand != 'X':
                    print('Currently', demand, 'is required\nChecking the stock inventory...')
                    attend_demand(demand)
                else:
                    print('Could not connect to hospital web server.\nPlease try again after some time.')
            elif choice == RECORD_NEW_DONATION:
                print('Record new donation')
            elif choice == STOCK_VISUAL_REPORT:
                print('Stock visual report')
            elif choice == EXIT:
                print('Have a good day.')
            else:
                print('Invalid choice! Please try again.')


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
    for each_donor in range(1, 100):
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
    for key, value in stock.items():
        # Return date collected corresponding to a date string in the format YYYY-MM-DD
        date_collected = date.fromisoformat(value[-1])
        today = date.today()  # Set today's date
        bag_age = (today - date_collected).days  # Calculate difference in number of days
        stock[key] += [str(bag_age)]  # Add a new field for days old to the dictionary and convert it to string
        bag_age = int(value[-1])  # Convert the age of the bag value to integer
        if bag_age > 30:  # Search for any bags older than 30 days
            print(key)  # Display the ID
    # donors_update, stock_update = save_db(DONORS_FILE, BAGS_FILE)


def attend_demand(blood_type):
    """ This function displays what blood group is available in the database """
    donors_dict, stock_dict = load_db(DONORS_FILE, BAGS_FILE)
    stock = open(BAGS_FILE, 'r')  # Create file handler to open bags.txt in read-mode
    for bag_id, blood in stock_dict.items():
        # each_bag_list = each_bag.strip().split(',')  # Convert line to list, remove redundant spaces
        # bag_id = each_bag_list[0]  # Assign bag_id to first index in list
        # blood_group = each_bag_list[1]  # Assign blood_group to second index in list
        # # Search for the blood group in the blood compatibility dictionary
        # if blood_group in str(blood_compatibility[blood_type]):
        #     print('Following bag should be supplied\nID: ' + bag_id + ' (' + blood_group + ')')
        #     break  # break to print only the first blood group found
        # else:
        #     print('Sorry, an eligible donor does not exist in the database.')
        #     # break

        # print(id, blood[0])
        if blood[0] in blood_compatibility[blood_type]:
            print('Following bag should be supplied\nID: ' + str(bag_id) + ' (' + str(blood[0]) + ')')
            break
        # else:
        #     print('Sorry, an eligible donor does not exist in the database.')



# main()
attend_demand('B+')
# check_inventory()
# save_db(DONORS_NEW_FILE, BAGS_NEW_FILE)
# print(blood_compatibility['AB+'])
# fh = open('bags.txt')
# for line in fh:
#     linelst = line.strip().split(',')
#     print(linelst)
#     if linelst[1] in str(blood_compatibility['AB+']):
#         found = linelst[1]
#         print(found)
#         break
