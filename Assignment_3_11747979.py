""" LifeServe Blood Institute (lBI) blood-group program """

import sys
import matplotlib.pyplot as plt
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
blood_table = {'O-': ['O-'],
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
        # Concatenate filename with extension so that user does not have to enter it and strip to remove extra spaces
        donors_db = donors_db.strip() + '.txt'
    stock_db = input('Stock inventory database (bags): ').lower()
    if len(stock_db) == 0:
        stock_db = BAGS_FILE
    else:
        stock_db = stock_db.strip() + '.txt'

    donor_dict, stock_dict = load_db(donors_db, stock_db)
    if load_db(donors_db, stock_db):  # Confirm that the files are loaded successfully
        print('Database loaded successfully\n')

        try:
            choice = 0  # Hold the user's menu choice
            while choice != EXIT:
                # Display the menu
                display_menu()

                choice = int(input('Enter your choice: '))  # Get the user's choice
                print()
                if choice == CHECK_INVENTORY:
                    new_stock = check_inventory(stock_dict)  # Call the check_inventory function
                    input('Please dispose of them. Press [Enter] when done... ')
                    save_db(donor_dict, new_stock)  # Call the save_db() function to save the data into file
                    print('Updated database files saved to disk.')
                elif choice == ATTEND_BLOOD_DEMAND:
                    demand = check_demand()
                    if demand != 'X':
                        print('Currently', demand, 'is required\nChecking the stock inventory...\n')
                        attend_demand(demand, donor_dict, stock_dict)  # Call the attend to blood demand function
                    else:
                        print('Could not connect to hospital web server.\nPlease try again after some time.\n')
                elif choice == RECORD_NEW_DONATION:
                    unique_id = int(input('Enter the donor\'s unique ID: '))
                    record_donation(unique_id, donor_dict, stock_dict)  # Call the record_donation() function
                elif choice == STOCK_VISUAL_REPORT:
                    visual_report(stock_dict)  # Call the visual_report() function
                elif choice == EXIT:
                    print('Have a good day.')
                else:
                    print('Invalid choice! Please try again.')
        except ValueError:  # Catch any invalid input
            sys.exit('Invalid input. System exiting...\n')


def load_db(donor_fname, stock_fname):
    """ This function takes in two file names as parameters, reads both files and stores their data in a dictionary """
    donor_dict = {}  # Create an empty donor dictionary
    try:
        donor_file = open(donor_fname, 'r')
        for each_donor in donor_file:
            each_donor = each_donor.strip().split(',')  # Remove leading and trailing characters and split
            # Get each field individually
            donor_id = int(each_donor[0])
            donor_name = each_donor[1]
            phone = each_donor[2]
            email = each_donor[3]
            blood_group = each_donor[4]
            last_donation_date = each_donor[5]
            # Append data to dictionary
            donor_dict[donor_id] = [donor_name, phone, email, blood_group, last_donation_date]
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
            stock_dict[bag_id] = [blood_group, date_collected]  # Append data to dictionary

        stock_file.close()

    except FileNotFoundError:
        sys.exit('No such file or directory')

    except IOError:
        sys.exit('Some error in the file I/O occurred')

    except:  # Generic handler to capture any other unspecified error
        sys.exit('Something went wrong')

    return donor_dict, stock_dict  # Return the donor and stock dictionary


def save_db(donor_fname, stock_fname):
    """ This function updates the donor and bags files, and saves them into new files """
    try:
        stock_file = open(BAGS_NEW_FILE, 'w')  # open the bags-new.txt file in write mode
        for bag_id, bag_details in stock_fname.items():
            value_str = ",".join(map(str, bag_details))  # Convert the value list into a string of characters
            stock_file.write(str(bag_id) + ',' + value_str + '\n')

        stock_file.close()

    except IOError:
        sys.exit('Some error in the file I/O occurred')

    except TypeError:
        sys.exit('Invalid data type')

    except ValueError:
        sys.exit('Too many values to unpack')

    try:
        donor_file = open(DONORS_NEW_FILE, 'r+')  # open the donor-new.txt file in read-write mode
        for donor_id, donor_details in donor_fname.items():
            name = donor_details[0]
            phone = donor_details[1]
            email = donor_details[2]
            blood_group = donor_details[3]
            last_donation_date = donor_details[4]
            # Write the updated data from the dictionary to file
            donor_file.write(str(donor_id) + ',' + name + ',' + phone + ',' + email + ',' + blood_group + ',' +
                             last_donation_date + '\n')

        donor_file.close()

    except IOError:
        sys.exit('Some error in the file I/O occurred')

    except TypeError:
        sys.exit('Invalid data type')

    except ValueError:
        sys.exit('Too many values to unpack')


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


def check_inventory(stock_dictionary):
    """ This function searches for any bags older than 30 days, and if found, it displays their ID numbers so that staff
     can dispose of them """
    print('Following bags are out of their use-by date')
    for key, value in stock_dictionary.items():
        # Return date collected corresponding to a date string in the format YYYY-MM-DD
        date_collected = date.fromisoformat(value[1])
        today = date.today()  # Set today's date
        bag_age = (today - date_collected).days  # Calculate difference in number of days
        # Add a new field for days old to the dictionary
        stock_dictionary[key] += [bag_age]
        bag_age = value[-1]  # Assign age of bag to the last position in the value list
        if bag_age > 30:  # Search for any bags older than 30 days
            print(key)  # Display the ID

    # Create a new dictionary with the updated stock records
    new_stock_dict = {k: v[:-1] for k, v in stock_dictionary.items() if v[-1] < 30}

    return new_stock_dict


def attend_demand(blood_type, donors_dict, stock_dict):
    """ This function searches for available blood group in the database and find a list of eligible donors with
    compatible blood type whom staff can contact. If no eligible donors exist, it notifies the staff """
    for bag_id, bag_details in stock_dict.items():
        # Check if value at index[0] in the list is in the blood_table dictionary
        if bag_details[0] in blood_table[blood_type]:
            print('Following bag should be supplied\nID: ' + str(bag_id) + ' (' + bag_details[0] + ')\n')
            # Create a new stock dictionary with dispatched bag removed from database, which is later saved to file
            new_stock = {k: v for k, v in stock_dict.items() if k != bag_id}
            input('Press [Enter] once it is packed for dispatch... ')
            save_db(donors_dict, new_stock)  # Call the save_db() function
            print('Inventory records updated.\nUpdated database files saved to disk.\n')
            break  # break to print only the first blood group found
    else:
        # No eligible donor exists
        print('We can not meet the requirement. Checking the donor database...\n')
        print('Following donors match the requirements. Please contact them for new donation.\n')
        for donor_id, donor_details in donors_dict.items():
            # Give each index a variable name
            name = donor_details[0]
            phone = donor_details[1]
            email = donor_details[2]
            if donor_details[3] in blood_table[blood_type]:
                print('• ' + name + ', ' + phone + ', ' + email + '\n')


def record_donation(donor_unique_id, donors_dic, stock_dic):
    """ This function allows staff to check for available donors and add a new bag to the database """
    date_today = date.today()  # Set today's date
    for donor_id, donor_details in donors_dic.items():
        # Return last donation date corresponding to a date string in the format YYYY-MM-DD
        last_donation = date.fromisoformat(donor_details[4])
        age_of_donation = (date_today - last_donation).days  # Calculate difference in number of days
        # Add a new field for donation age to the dictionary
        donors_dic[donor_id] += [age_of_donation]
        age_of_donation = donor_details[-1]
        if donors_dic.get(donor_unique_id) is None:  # If donor id is not found in the database
            print('That ID does not exist in the database.\nTo register a new donor, please contact the system '
                  'administrator.\n')
            break
        # Ineligible if donation age is greater than 120 days from the last donation
        elif donor_id == donor_unique_id and age_of_donation >= 120:
            print('Sorry, this donor is not eligible for donation.\n')
            break
    else:
        # If eligible, add a new bag with the current date and new autogenerated ID
        print('Recording a new donation with following details:')
        for donor_id, donor_details in donors_dic.items():
            donor_name = donor_details[0]
            donor_blood_group = donor_details[3]
            last_donation_date = date_today.isoformat()  # Convert date object to ISO format
            if donor_id == donor_unique_id:
                print('From: ', donor_name)
                print('Group: ', donor_blood_group)
                print('Date: ', date_today)
                donors_dic[donor_id][4] = last_donation_date  # Update donor's last donation date
                add_bag(donor_blood_group)  # Call the add_bag function
                save_db(donors_dic, stock_dic)  # Call the save_db() function
                break


def visual_report(bags_file):
    """ This function allows the user to see the distribution of in-stock blood bags in the form of a pie chart """
    # Initialise the blood group count values to zero
    count_O_neg, count_O_pos, count_B_neg, count_B_pos = 0, 0, 0, 0
    count_A_neg, count_A_pos, count_AB_neg, count_AB_pos = 0, 0, 0, 0

    report_dict = {}  # Create an empty dictionary to store the total count of blood per group

    # Count the number of occurrences of blood per group
    for key, value in bags_file.items():
        blood_group = value[0]
        if blood_group == 'O-':
            count_O_neg += 1
            report_dict['O-'] = count_O_neg
        elif blood_group == 'O+':
            count_O_pos += 1
            report_dict['O+'] = count_O_pos
        elif blood_group == 'B-':
            count_B_neg += 1
            report_dict['B-'] = count_B_neg
        elif blood_group == 'A-':
            count_A_neg += 1
            report_dict['A-'] = count_A_neg
        elif blood_group == 'A+':
            count_A_pos += 1
            report_dict['A+'] = count_A_pos
        elif blood_group == 'AB-':
            count_AB_neg += 1
            report_dict['AB-'] = count_AB_neg
        elif blood_group == 'AB+':
            count_AB_pos += 1
            report_dict['AB+'] = count_AB_pos
        else:
            report_dict = {}

    # Create list of labels and values from dictionary
    labels = [key for key in report_dict.keys()]
    values = [value for value in report_dict.values()]

    # Format the labels and values
    label_value = ['{} ({:,.0f})'.format(label, value) for label, value in zip(labels, values)]

    # Plot the pie-chart
    plt.pie(values, labels=label_value)
    plt.show()


def add_bag(blood_group):
    """ This function adds a new bag to the database """
    try:
        new_bags_file = open(BAGS_NEW_FILE, 'r+')
        today = date.today()  # Set the current date
        current_date = today.isoformat()  # Convert date object to ISO format
        # Get the next bag ID in the database and increment by one
        bag_id = max([int(line.split(',')[0]) for line in new_bags_file]) + 1
        print('Bag ID:', bag_id)
        confirm_save = input('Please confirm (y/n): ').lower()
        if confirm_save == 'y':
            new_bags_file.write(str(bag_id) + ',' + blood_group + ',' + current_date + '\n')
            print('Done. Donor\'s last donation date also updated to', current_date)
            print('Updated database files saved to disk.\n')
        elif confirm_save == 'n':
            print('Cancelled.')
        else:
            print('Invalid choice\n')
        new_bags_file.close()
    except ValueError:
        print('File is empty')


main()
# donors, stock = load_db(DONORS_FILE, BAGS_FILE)
# d = check_demand()
# visual_report(stock)
# print(donors)
# attend_demand(d, donors, stock)
# record_donation(num)
# ch = check_inventory(stock)
# add_bag('O-')
