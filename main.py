import json
import os

class Suburb:
    def __init__(self, name, resources, evacuation_centers, evacuation_orders, connections):
        self.name = name
        self.resources = resources
        self.evacuation_centers = evacuation_centers
        self.evacuation_orders = evacuation_orders
        self.connections = connections

class Player:
    def __init__(self, name, role='guest'):
        self.name = name
        self.role = role
        self.inventory = {}
        self.current_location = None

class EmergencySystem:
    def __init__(self, suburbs_file):
        self.suburbs = self.load_suburbs(suburbs_file)
        self.suburb_map = {s.name: s for s in self.suburbs}
        self.player = None
    
    def load_suburbs(self, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Error: Missing {filename} file!")
            exit()
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}")
            exit()
            
        suburbs = []
        for item in data:
            suburbs.append(Suburb(
                item['name'],
                item.get('resources', {}),
                item.get('evacuation_centers', []),
                item.get('evacuation_orders', []),
                item.get('connections', {})
            ))
        return suburbs

    def login(self, username, password):
        if username == "admin" and password == "flood2024":
            self.player = Player(username, 'admin')
        else:
            self.player = Player(username)
        
        # Dynamic starting location
        default_start = 'Headquarters'
        start_location = self.suburb_map.get(default_start, self.suburbs[0] if self.suburbs else None)

        if start_location:
            self.player.current_location = start_location
            print(f"Starting at: {self.player.current_location.name}")
        else:
            print("Error: No starting suburb found!")
            exit()

        return True

    def process_command(self, command):
        cmd = command.lower().split()
        if not cmd:
            return True
        
        action = cmd[0]
        if action == "go":
            self.handle_movement(cmd[1] if len(cmd) > 1 else None)
        elif action == "take":
            self.handle_take(cmd[1:])
        elif action == "drop":
            self.handle_drop(cmd[1:])
        elif action == "look":
            self.describe_location()
        elif action == "inventory":
            self.show_inventory()
        elif action == "exit":
            print("Exiting system...")
            return False
        else:
            print("Invalid command. Available commands: go, take, drop, look, inventory, exit")
        return True

    def handle_movement(self, direction):
        valid_directions = ['north', 'south', 'east', 'west']
        if not direction or direction not in valid_directions:
            print("Specify valid direction (north/south/east/west)")
            return
        
        current = self.player.current_location
        new_loc = current.connections.get(direction)
        if new_loc:
            self.player.current_location = self.suburb_map[new_loc]
            print(f"Moved to {new_loc}")
        else:
            print("Cannot move in that direction")

    def handle_take(self, args):
        if self.player.role != 'admin':
            print("Only admins can take resources")
            return
        
        if len(args) < 1:
            print("Specify item to take")
            return
        
        item = args[0].lower()
        quantity = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
        
        if self.player.current_location.resources.get(item, 0) >= quantity:
            self.player.current_location.resources[item] -= quantity
            if self.player.current_location.resources[item] == 0:
                del self.player.current_location.resources[item]
            self.player.inventory[item] = self.player.inventory.get(item, 0) + quantity
            print(f"Took {quantity} {item}(s)")
        else:
            print("Not enough resources available")

    def handle_drop(self, args):
        if self.player.role != 'admin':
            print("Only admins can drop resources")
            return
        
        if len(args) < 1:
            print("Specify item to drop")
            return
        
        item = args[0].lower()
        quantity = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
        
        if self.player.inventory.get(item, 0) >= quantity:
            self.player.inventory[item] -= quantity
            if self.player.inventory[item] == 0:
                del self.player.inventory[item]
            self.player.current_location.resources[item] = self.player.current_location.resources.get(item, 0) + quantity
            print(f"Dropped {quantity} {item}(s)")
        else:
            print("Not enough in inventory")

    def describe_location(self):
        loc = self.player.current_location
        print(f"\nCurrent Location: {loc.name}")
        print("Resources available:", loc.resources or "None")
        print("Evacuation Centers:")
        if loc.evacuation_centers:
            for ec in loc.evacuation_centers:
                features = []
                if ec.get('pet_friendly'): features.append("Pets allowed")
                if ec.get('catered'): features.append("Catered")
                if ec.get('overnight'): features.append("Overnight stay")
                print(f"- {ec['address']}: {', '.join(features)}")
        else:
            print("None")
        print("Active evacuation orders:", loc.evacuation_orders or "None")
        print("Available directions:", list(loc.connections.keys()) or "None")

    def show_inventory(self):
        print("Current inventory:", self.player.inventory or "Empty")

def main():
    system = EmergencySystem("suburbs.json")
    print("=== Flood Emergency Management System ===")
    
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip() if username == "admin" else ""
        if system.login(username, password):
            break
        print("Invalid login")
    
    running = True
    while running:
        system.describe_location()
        command = input("\nEnter command: ").strip()
        running = system.process_command(command)

if __name__ == "__main__":
    main()
