"""
This program manages shoe inventory. It allows users to do the following:
- Read data from the 'inventory.txt' file.
- Add new shoes to the inventory.
- View all shoes in the inventory.
- Restock shoes with low quantity.
- Search for a specific shoe.
- Calculate the value of each shoe.
- Find the shoe with the highest quantity.
The program makes use of the Shoe class to represent individual shoes and 
maintians a list of Shoe objects to manage the inventory.
"""

#========The beginning of the class==========


class Shoe:

    # The following represents a shoe in the inventory:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    # Add the code to return the cost of the shoe in this method.    
    def get_cost(self):
        return self.cost    

    # Add the code to return the quantity of the shoes.
    def get_quantity(self):
        return self.quantity

    # Add a code to returns a string representation of a class.
    def __str__(self):
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"


#=============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []


#==========Functions outside the class==============
# Read the shoe data from the inventory file and create Shoe objects.
# This function also appends the created objects to the 'shoe_list'.
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as file:
            next(file)
            for line in file:
                data = line.strip().split(", ")
                if len(data) == 5:
                    country, code, product, cost, quantity = data
                    try:
                        cost = float(cost)
                        quantity = int(quantity)
                    except ValueError:
                        print(f"\nError: Invalid data format in line: {line.strip()}\n".upper())
                        continue
                    shoe = Shoe(country, code, product, cost, quantity)
                    shoe_list.append(shoe)
        print("\nThe data has been loaded successfully!\n".upper())
    except FileNotFoundError:
        print("\nThe file in question has not been found!\n".upper())
    except Exception as e:
        print(f"\nAn error occurred: {e}\n")


# This captures data for a new shoe and adds it to the inventory.
# I know the 'while True' loops could be reduced, however, it is coded this
# way for end-user ease.
# The instructions did not specify to add the new shoe to the 'inventory.txt' file.
# Only to add the new show to the 'shoe_list'.
def capture_shoes():
    while True:
        country = input("Enter the country: ").strip()
        if country:
            break
        print("\nCountry cannot be empty. Please try again\n".upper())

    while True:    
        code = input("Enter the shoe code: ").strip()
        if code:
            break
        print("\nError: Shoe code cannot be empty. Please try again.\n".upper())

    while True:    
        product = input("Enter the product: ").strip()
        if product:
            break
        print("\nError: Product name cannot be empty. Please try again.\n".upper())
    
    while True:
        try:
            cost = float(input("Enter the cost: "))
            if cost < 0:
                raise ValueError("\nThe cost cannot be negative.\n".upper())
            break
        except ValueError as e:
            print(f"\nInput error: {e} Please enter a valid positive number.\n".upper())

    while True:
        try:
            quantity = int(input("Enter the quantity: "))
            if quantity < 0:
                raise ValueError("Quantity cannot be a negative integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e} Please enter a valid positive integer.\n".upper())

    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)
    print("\nThe shoe has been added successfully!\n".upper())
    

# This section displays all shoes in the inventory.
# This function prints the details of all the shoes in the 'shoe_list'.
# I should have used the tabulate module...
def view_all():
    if not shoe_list:
        print("\nThere are no shoes in the inventory.\n".upper())
        return
    
    print("Country | Code | Product | Cost | Quantity")
    print(50 * "-")
    for shoe in shoe_list:
        print(f"{shoe.country} | {shoe.code} | {shoe.product} | {shoe.cost} | {shoe.quantity}")
    

# This function finds the shoe with the lowest quantity and asks the user if they would like to restock.
# It then updates the inventory file.
def re_stock():
    if not shoe_list:
        print("\nThere are no shoes in the inventory.\n".upper())
        return

    min_quant_shoe = min(shoe_list, key=lambda x: x.quantity)
    print(f"\nThe shoe with the lowest quantity is {min_quant_shoe}\n")
    while True:
        add_quantity = input("\nEnter the quantity you wish to add or press 'Enter' to skip: ")
        if not add_quantity:
            print("No changes have been made.")
            return

        try:
            add_quantity = int(add_quantity)
            if add_quantity < 0:
                raise ValueError("\nThe quantity cannot be negative\n".upper())
            break
        except ValueError as e:
            print(f"\nInput error: {e} Please enter a valid positive integer.\n".upper())
    
    min_quant_shoe.quantity += add_quantity
    print("\nQuantity updated successfully\n".upper())

    #Update the 'inventory' file:
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

        with open("inventory.txt", "w") as file:
            file.write(lines[0])    # This writes the header.
            for shoe in shoe_list:
                file.write(f"{shoe}\n")

        print("\nThe file updated successfully\n".upper())
    
    except FileNotFoundError:
        print("\nError: The inventory file was not found.\n".upper())
    except Exception as e:
        print(f"\nAn error occurred while updating the file: {e}\n".upper())


# This function asks the user for a shoe code and displays the related details.
def search_shoe():
    if not shoe_list:
        print("\nThere are no shoes in the inventory.\n".upper())
        return

    code = input("\nPlease enter the shoe code to search:\n")
    for shoe in shoe_list:
        if shoe.code == code:
            print(f"The shoe has been found: {shoe}")
            return
    print("\nSorry, no shoe has been found!\n".upper())    
    

# Calculate and display the value of each shoe item.
def value_per_item():
    if not shoe_list:
        print("\nThere are no shoes in the inventory\n".upper())
        return

    print("Product | Value")
    print(20 * "-")
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        print(f"{shoe.product} | {value:.2f}")
    

# This function finds the shoe with the highest quantity and displays that it is for sale.
def highest_qty():
    if not shoe_list:
        print("\nThere are no shoes in the inventory.\n".upper())
        return

    max_quant_shoe = max(shoe_list, key=lambda x: x.quantity)
    print(f"The shoe with the highest quantity: {max_quant_shoe.product}")    
    print("\nThis shoe is for sale!\n".upper())


#==========Main Menu=============
def main_menu():
    while True:
        print("""
===== Shoe Inventory Management System =====
1. Read shoes data
2. Capture shoes
3. View all shoes
4. Re-stock shoes
5. Search for a shoe
6. Calculate value per item
7. Find shoe with highest quantity
8. Exit
              """)
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            read_shoes_data()
        elif choice == "2":
            capture_shoes()
        elif choice == "3":
            view_all()
        elif choice == "4":
            re_stock()
        elif choice == "5":
            search_shoe()
        elif choice == "6":
            value_per_item()
        elif choice == "7":
            highest_qty()
        elif choice == "8":
            print("Thank you for using the Shoe Inventory Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
