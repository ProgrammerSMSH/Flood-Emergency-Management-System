import json  # Importing the JSON module to handle JSON files
import os  # Importing the os module for operating system dependent functionalities

# Class to represent a suburb
class Suburb:
    # Constructor to initialize the suburb's attributes
    def __init__(self, name, resources, evacuation_centers, evacuation_orders, connections):
        self.name = name  # Name of the suburb
        self.resources = resources  # Resources available in the suburb
        self.evacuation_centers = evacuation_centers  # Evacuation centers in the suburb
        self.evacuation_orders = evacuation_orders  # Evacuation orders for the suburb
        self.connections = connections  # Directions to other connected suburbs

# Class to represent a player
class Player:
    # Constructor to initialize player's attributes
    def __init__(self, name, role='guest'):
        self.name = name  # Name of the player
        self.role = role  # Role of the player, default is 'guest'
        self.inventory = {}  # Inventory of the player
        self.current_location = None  # Current location of the player

# Class to handle the emergency system
class EmergencySystem:
    # Constructor to initialize the emergency system with suburbs and the player
    def __init__(self, suburbs_file):
        self.suburbs = self.load_suburbs(suburbs_file)  # Load suburbs from the JSON file
        self.suburb_map = {s.name: s for s in self.suburbs}  # Create a map of suburb names to suburb objects
        self.player = None  # Initialize the player as None

    # Method to load suburbs from a JSON file
    def load_suburbs(self, filename):
        try:
            with open(filename) as f:  # Open the JSON file
                data = json.load(f)  # Load the data from the file
        except FileNotFoundError:  # Handle the case where the file is not found
            print(f"Error: Missing {filename} file!")
            exit()  # Exit if file is missing
        except json.JSONDecodeError as e:  # Handle errors in JSON decoding
            print(f"Invalid JSON: {e}")
            exit()  # Exit if the JSON is invalid
            
        suburbs = []  # List to store suburb objects
        for item in data:  # Loop through each item in the loaded data
            suburbs.append(Suburb(
                item['name'],  # Name of the suburb
                item.get('resources', {}),  # Resources of the suburb (default empty dictionary)
                item.get('evacuation_centers', []),  # Evacuation centers (default empty list)
                item.get('evacuation_orders', []),  # Evacuation orders (default empty list)
                item.get('connections', {})  # Connections (default empty dictionary)
            ))
        return suburbs  # Return the list of suburb objects

    # Method for player login
    def login(self, username, password):
        if username == "admin" and password == "flood2024":  # Check if credentials are correct for admin
            self.player = Player(username, 'admin')  # Create player with 'admin' role
        else:
            self.player = Player(username)  # Create player with 'guest' role if not admin
        
        # Set dynamic starting location for the player
        default_start = 'Headquarters'  # Default start location
        start_location = self.suburb_map.get(default_start, self.suburbs[0] if self.suburbs else None)  # Find start location
        
        if start_location:  # If a valid start location is found
            self.player.current_location = start_location  # Set player's starting location
            print(f"Starting at: {self.player.current_location.name}")  # Print the starting location
        else:
            print("Error: No starting suburb found!")  # Print error if no start location
            exit()  # Exit the program

        return True  # Return True for successful login

    # Method to process commands entered by the player
    def process_command(self, command):
        cmd = command.lower().split()  # Split the command into words and convert to lowercase
        if not cmd:  # If no command is entered, return True to keep running
            return True
        
        action = cmd[0]  # First word is the action (command)
        if action == "go":  # If the action is 'go', handle movement
            self.handle_movement(cmd[1] if len(cmd) > 1 else None)
        elif action == "take":  # If the action is 'take', handle taking resources
            self.handle_take(cmd[1:])
        elif action == "drop":  # If the action is 'drop', handle dropping resources
            self.handle_drop(cmd[1:])
        elif action == "look":  # If the action is 'look', describe the current location
            self.describe_location()
        elif action == "inventory":  # If the action is 'inventory', show the player's inventory
            self.show_inventory()
        elif action == "exit":  # If the action is 'exit', exit the system
            print("Exiting system...")
            return False
        else:
            print("Invalid command. Available commands: go, take, drop, look, inventory, exit")  # Invalid command
        return True  # Continue running

    # Method to handle movement between suburbs
    def handle_movement(self, direction):
        valid_directions = ['north', 'south', 'east', 'west']  # Define valid directions
        if not direction or direction not in valid_directions:  # If direction is not valid, print message
            print("Specify valid direction (north/south/east/west)")
            return
        
        current = self.player.current_location  # Get the player's current location
        new_loc = current.connections.get(direction)  # Get the connected suburb in the given direction
        if new_loc:  # If a valid connection exists in that direction
            self.player.current_location = self.suburb_map[new_loc]  # Move player to the new location
            print(f"Moved to {new_loc}")  # Print the new location
        else:
            print("Cannot move in that direction")  # If no valid connection, print message

    # Method to handle taking resources from the current location
    def handle_take(self, args):
        if self.player.role != 'admin':  # Only admins can take resources
            print("Only admins can take resources")
            return
        
        if len(args) < 1:  # If no resource is specified, print message
            print("Specify item to take")
            return
        
        item = args[0].lower()  # Get the item to take
        quantity = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1  # Get the quantity (default 1)

        if self.player.current_location.resources.get(item, 0) >= quantity:  # Check if enough resources are available
            self.player.current_location.resources[item] -= quantity  # Deduct the resources from the location
            if self.player.current_location.resources[item] == 0:  # If no resources left, remove item
                del self.player.current_location.resources[item]
            self.player.inventory[item] = self.player.inventory.get(item, 0) + quantity  # Add item to player's inventory
            print(f"Took {quantity} {item}(s)")  # Print success message
        else:
            print("Not enough resources available")  # If not enough resources, print message

    # Method to handle dropping resources
    def handle_drop(self, args):
        if self.player.role != 'admin':  # Only admins can drop resources
            print("Only admins can drop resources")
            return
        
        if len(args) < 1:  # If no item is specified, print message
            print("Specify item to drop")
            return
        
        item = args[0].lower()  # Get the item to drop
        quantity = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1  # Get the quantity (default 1)

        if self.player.inventory.get(item, 0) >= quantity:  # Check if the player has enough of the item
            self.player.inventory[item] -= quantity  # Deduct the resources from the player's inventory
            if self.player.inventory[item] == 0:  # If no resources left, remove item
                del self.player.inventory[item]
            self.player.current_location.resources[item] = self.player.current_location.resources.get(item, 0) + quantity  # Add item to location
            print(f"Dropped {quantity} {item}(s)")  # Print success message
        else:
            print("Not enough in inventory")  # If not enough in inventory, print message

    # Method to describe the current location of the player
    def describe_location(self):
        loc = self.player.current_location  # Get the player's current location
        print(f"\nCurrent Location: {loc.name}")  # Print the name of the location
        print("Resources available:", loc.resources or "None")  # Print available resources in the location
        print("Evacuation Centers:")  # List the evacuation centers
        if loc.evacuation_centers:  # If there are evacuation centers, list them
            for ec in loc.evacuation_centers:
                features = []
                if ec.get('pet_friendly'): features.append("Pets allowed")  # If pet-friendly, add to features
                if ec.get('catered'): features.append("Catered")  # If catered, add to features
                if ec.get('overnight'): features.append("Overnight stay")  # If overnight, add to features
                print(f"- {ec['address']}: {', '.join(features)}")  # Print the evacuation center details
        else:
            print("None")  # Print "None" if no evacuation centers
        print("Active evacuation orders:", loc.evacuation_orders or "None")  # Print active evacuation orders
        print("Available directions:", list(loc.connections.keys()) or "None")  # Print available directions

    # Method to show the player's inventory
    def show_inventory(self):
        print("Current inventory:", self.player.inventory or "Empty")  # Print the player's inventory or "Empty"

# Main function to run the emergency system
def main():
    system = EmergencySystem("suburbs.json")  # Create an EmergencySystem object with the suburbs file
    print("=== Flood Emergency Management System ===")  # Print system title
    
    while True:  # Loop for login
        username = input("Username: ").strip()  # Get username input
        password = input("Password: ").strip() if username == "admin" else ""  # Get password if username is admin
        if system.login(username, password):  # Attempt to login
            break  # If login is successful, exit the loop
        print("Invalid login")  # Print message if login fails
    
    running = True  # Variable to keep the system running
    while running:  # Main game loop
        system.describe_location()  # Describe the current location
        command = input("\nEnter command: ").strip()  # Get command input
        running = system.process_command(command)  # Process the command and decide whether to continue running

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
