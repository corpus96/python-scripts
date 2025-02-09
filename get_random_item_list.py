import random

filename = "lists.txt"

with open(filename, "r") as file:
    items = [line.strip() for line in file.readlines()]

while True:
    if not items:
        print("The list is empty, exit program")
        break

    random_item = random.choice(items)
    print(f"\Randomly selected item: {random_item}")
    response = input("Do you want to remove this item? (yes/no) or type 'exit' to quit: ").strip().lower()

    if response == "yes" or response == "y" or response == "Y" or response == "YES":
        items.remove(random_item)
        print(f"The item '{random_item}' has been removed.")
    elif response == "no" or response == "NO" or response == "n" or response == "N":
        print(f"The item '{random_item}' was not removed.")
    elif response == "exit" or response == 'e':
        print("Exiting the program")
        break
    else:
        print("Invalid input.")
