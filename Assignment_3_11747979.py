""" LifeServe Blood Institute (lBI) blood-group program """

# Main menu choices
CHECK_INVENTORY = 1
ATTEND_BLOOD_DEMAND = 2
RECORD_DONATION = 3
STOCK_VISUAL_REPORT = 4
EXIT = 5
# Create a blood-group transfusion compatibility table in the form of a dictionary
blood_compatibility = {'O-': ['O-'], 'O+': ['0-', 'O+'], 'B-': ['O-', 'B-'], 'B+': ['O-', 'O+', 'B-', 'B+'],
                       'A-': ['O-', 'A-'], 'A+': ['O-', 'O+', 'A-', 'A+'], 'AB-': ['O-', 'B-', 'A-', 'AB-'],
                       'AB+': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+']}


def load_db(donor_fname, stock_fname):
    donor_file = open(donor_fname, 'r')
    for line in donor_file:
        line = line.strip().split(',')
    donor_file.close()

    stock_file = open(stock_fname, 'r')
    for line in stock_file:
        line = line.strip().split(',')
    stock_file.close()


def save_db(donor_fname, stock_fname):
    donor_file = open(donor_fname, 'w')
    donor_file.close()

    bags_file = open(stock_fname, 'w')
    bags_file.close()


def main():
    print('<<< LifeServe Blood Institute >>>\n')
    print('Loading database...')
    print('Enter the database file names without .txt extension\nor just press Enter to accept defaults')
    try:
        donors_db = input('Donors database (donors): ')
        donors_db = donors_db + '.txt'
        stock_db = input('Stock inventory database (bags): ')
        stock_db = stock_db + '.txt'
        load_db(donors_db, stock_db)
        print('Database loaded successfully\n')

        choice = 0  # Hold the user's menu choice
        while choice != EXIT:
            # Display the menu
            display_menu()

            choice = int(input('Enter your choice: '))  # Get the user's choice

    except FileNotFoundError:
        print('No such file or directory')
    except IOError:
        print('Some error in the file I/O occured')
    except:  # Generic handler to
        print('Something went wrong')
        # save_db('donors-new.txt', 'bags-new.txt')


def display_menu():
    print('------------')
    print('Main Menu')
    print('------------')
    print('(1) Check inventory')
    print('(2) Attend to blood demand')
    print('(3) Record new donation')
    print('(4) Stock visual report')
    print('(5) Exit')


main()
# d = {}
# l = []
# f = open('donors.txt', 'r')
# for line in f:
#     # print(line.strip().split(','))
#     l.append(line.strip().split(','))
#     key = int(line[0])
#     # name, num = line[2], line[3]
# print(l[0])
