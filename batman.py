import os
import time

def clear_screen():
    """Clears the console screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    """Displays the main menu options."""
    print("================= Medibolt =================")
    print("1. Manage Medical Records")
    print("2. Schedule Appointments")
    print("3. Doctor Dashboard")
    print("4. Exit")
    print("===========================================")
    choice = input("Select an option (1-4): ")
    return choice

def manage_medical_records():
    """Simulates managing medical records."""
    clear_screen()
    print("==== Manage Medical Records ====")
    print("1. Upload Medical Record")
    print("2. View Medical Records")
    print("3. Delete a Medical Record")
    print("4. Back to Main Menu")
    print("================================")
    choice = input("Select an option (1-4): ")

    if choice == "1":
        print("Uploading a medical record...")
        time.sleep(1)
        print("Record uploaded successfully.")
    elif choice == "2":
        print("Fetching medical records...")
        time.sleep(1)
        print("No records found. [Sample Message]")
    elif choice == "3":
        print("Deleting a medical record...")
        time.sleep(1)
        print("Record deleted successfully.")
    elif choice == "4":
        return
    else:
        print("Invalid choice. Try again.")
    time.sleep(2)

def schedule_appointments():
    """Simulates scheduling appointments."""
    clear_screen()
    print("==== Schedule Appointments ====")
    print("1. Book an Appointment")
    print("2. View Upcoming Appointments")
    print("3. Cancel an Appointment")
    print("4. Back to Main Menu")
    print("================================")
    choice = input("Select an option (1-4): ")

    if choice == "1":
        print("Booking an appointment...")
        time.sleep(1)
        print("Appointment booked successfully.")
    elif choice == "2":
        print("Fetching upcoming appointments...")
        time.sleep(1)
        print("No upcoming appointments. [Sample Message]")
    elif choice == "3":
        print("Cancelling an appointment...")
        time.sleep(1)
        print("Appointment cancelled successfully.")
    elif choice == "4":
        return
    else:
        print("Invalid choice. Try again.")
    time.sleep(2)

def doctor_dashboard():
    """Simulates the doctor dashboard."""
    clear_screen()
    print("======= Doctor Dashboard =======")
    print("1. View Daily Appointments")
    print("2. Access Patient Records")
    print("3. Back to Main Menu")
    print("================================")
    choice = input("Select an option (1-3): ")

    if choice == "1":
        print("Fetching daily appointments...")
        time.sleep(1)
        print("No appointments for today. [Sample Message]")
    elif choice == "2":
        print("Accessing patient records...")
        time.sleep(1)
        print("No records available. [Sample Message]")
    elif choice == "3":
        return
    else:
        print("Invalid choice. Try again.")
    time.sleep(2)

def main():
    while True:
        clear_screen()
        choice = main_menu()

        if choice == "1":
            manage_medical_records()
        elif choice == "2":
            schedule_appointments()
        elif choice == "3":
            doctor_dashboard()
        elif choice == "4":
            print("Exiting Medibolt. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            time.sleep(2)

if __name__ == "__main__":
    main()
