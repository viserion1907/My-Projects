"""
LifeServe Blood Institute (LBI) is a small blood donation centre operating in a regional
Australian town. This program  can help LBI staff members quickly determine if a patient’s blood group is compatible
with that of a donor.
There are two major blood group systems – ABO and Rh. In the ABO system, the blood type can be one of the four: A, B,
AB, and O.
The Rh system defines two types: positive and negative, indicating the presence or absence of a specific antigen.
The following rules apply when checking transfusion compatibility
• If a recipient is Rh-negative, the donor must also be Rh-negative.
• If a recipient is Rh-positive, the donor can be either Rh-positive or Rh-negative.
This program allows the user to key in the ABO and Rh types of both the donor and the patient, and inform the user if
the recipient is allowed to get blood from that donor.
After each report, the program prompts the user for another check if needed. When the user chooses to finish, the
program will display the total number of checks performed, and what percentage of those were found to be compatible
"""

total_checks = 0  # accumulator variable to store the number of checks done
compatible_results = 0  # accumulator variable to store the number of compatible results
check = 'y'  # condition variable to prompt user if they want to continue running the program

while check == 'y' or check == 'Y':  # check whether user has typed Y/y
    print("Donor's Blood Group")  # Display heading
    # Prompt for the user's input, convert the blood group letters to uppercase for consistency
    donor_abo = input('\tABO Type: ').upper()  # ABO Type of the donor - priming read
    donor_rh = input('\tRh Type: ').upper()  # Rh Type of the donor - priming read
    print()
    print("Recipient's Blood Group")
    recipient_abo = input('\tABO Type: ').upper()  # ABO Type of the recipient - priming read
    recipient_rh = input('\tRh Type: ').upper()  # Rh Type of the recipient - priming read

    # Validate the user's input by checking that the right data was keyed in
    while (donor_abo != 'A' and donor_abo != 'AB' and donor_abo != 'B' and donor_abo != 'O') or (donor_rh != '+' and \
            donor_rh != '-') or (recipient_abo != 'A' and recipient_abo != 'AB' and recipient_abo != 'B' and \
            recipient_abo != 'O') or (recipient_rh != '+' and recipient_rh != '-'):
        # Generate an error message and prompt user to re-enter data
        print('\nERROR: Please check your ABO and/or Rh data (A, AB, or O)!')
        print("\nDonor's Blood Group")
        donor_abo = input('\tABO Type: ').upper()
        donor_rh = input('\tRh Type: ').upper()
        print("\nRecipient's Blood Group")
        recipient_abo = input('\tABO Type: ').upper()
        recipient_rh = input('\tRh Type: ').upper()

    # Check for ABO and Rh compatibility
    not_compatible = False  # create a flag variable (set to False) to check for incompatibility
    if donor_abo != "O" and recipient_abo != "AB" and donor_abo != recipient_abo:
        not_compatible = True
    if donor_rh != '-' and donor_rh != recipient_rh:
        if not_compatible:  # if not_compatible == True
            print('\n✗ Recipient’s blood is incompatible.')  # blood group and Rh factor do not match
        else:
            print('\n✗ Recipient’s blood is incompatible.')  # Rh factors do not match
    elif not_compatible:
        print('\n✗ Recipient’s blood is incompatible.')  # blood groups do not match
    else:
        print('\n✓ Recipient’s blood is compatible.')
        compatible_results += 1  # increment the compatible result by one

    check = input('\nDo you want another check (y/n)? ')  # ask user if they want another try
    total_checks += 1  # increment the total_checks variable by one

# Display the appropriate message for checks depending on if it was more than one or not
if total_checks < 2:
    print('\nA total of', total_checks, 'check was done.')
else:
    print('\nA total of', total_checks, 'checks were done.')

# calculate the compatible results by dividing it by total_checks and storing the results in compatible_results
compatible_results /= total_checks  # compatible_results = compatible_results / total_checks

# Print out the percentage of compatible results
print(format(compatible_results, '.1%'), 'of those returned a compatible result.\nThank you.')
