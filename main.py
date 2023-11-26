class Field:
    def __init__(self, field_name, area_size):
        self.field_name = field_name
        self.area_size = area_size
        self.cultures = {}  # словник для відстеження культур на полі
        self.work_schedule = {}  # графік робіт

    def plant_crops(self, culture_name, area):
        if culture_name in self.cultures:
            print(f"The culture '{culture_name}' is already planted on this field.")
        elif sum(self.cultures.values()) + area > self.area_size:
            print("Not enough free space on the field.")
        else:
            self.cultures[culture_name] = area
            print(f"Planted {area} hectares of '{culture_name}' on {self.field_name}.")

    def remove_crops(self, culture_name):
        if culture_name in self.cultures:
            area = self.cultures.pop(culture_name)
            print(f"Removed {area} hectares of '{culture_name}' from {self.field_name}.")
        else:
            print(f"No '{culture_name}' crops found on {self.field_name}.")

    def create_work_schedule(self, culture_name, work_schedule):
        if culture_name in self.cultures:
            if culture_name not in self.work_schedule:
                self.work_schedule[culture_name] = {}
            self.work_schedule[culture_name] = work_schedule
            print(f"Work schedule created for '{culture_name}' on {self.field_name}.")
        else:
            print(f"No '{culture_name}' crops found on {self.field_name}.")

    def edit_work_schedule(self, culture_name, new_work_schedule):
        if culture_name in self.work_schedule:
            self.work_schedule[culture_name] = new_work_schedule
            print(f"Work schedule updated for '{culture_name}' on {self.field_name}.")
        else:
            print(f"No work schedule found for '{culture_name}' on {self.field_name}.")

    def display_info(self):
        print(f"\nField: {self.field_name}")
        print(f"Total area: {self.area_size} hectares")
        print("Cultures:")
        for culture, area in self.cultures.items():
            print(f"  - {culture}: {area} hectares")
            if culture in self.work_schedule and self.work_schedule[culture] is not None:
                work_schedule_str = ', '.join(self.work_schedule[culture].keys())
                print(f"    Work Schedule: {work_schedule_str}")
        print()
    def edit_culture_area(self, culture_name, new_area):
        if culture_name in self.cultures:
            current_area = self.cultures[culture_name]
            total_area_except_current = sum(value for key, value in self.cultures.items() if key != culture_name)
            
            if total_area_except_current + new_area > self.area_size:
                print("Not enough free space on the field.")
            else:
                self.cultures[culture_name] = new_area
                print(f"Changed area for '{culture_name}' on {self.field_name} from {current_area} to {new_area} hectares.")
        else:
            print(f"No '{culture_name}' crops found on {self.field_name}.")     


class CultivatedField(Field):
    def __init__(self, field_name, area_size):
        super().__init__(field_name, area_size)

    def edit_work_schedule(self, culture_name, new_work_schedule):
        if culture_name in self.work_schedule:
            self.work_schedule[culture_name] = new_work_schedule
            print(f"Work schedule updated for '{culture_name}' on {self.field_name}.")
        else:
            print(f"No work schedule found for '{culture_name}' on {self.field_name}.")

    def delete_work_schedule(self, culture_name):
        if culture_name in self.work_schedule:
            del self.work_schedule[culture_name]
            print(f"Work schedule deleted for '{culture_name}' on {self.field_name}.")
        else:
            print(f"No work schedule found for '{culture_name}' on {self.field_name}.")


class FarmPlanner:
    def __init__(self):
        self.fields = {}

    def create_field(self, field_name, area_size, cultivated=False):
        if field_name not in self.fields:
            field_type = CultivatedField if cultivated else Field
            self.fields[field_name] = field_type(field_name, area_size)
            print(f"Field '{field_name}' created with {area_size} hectares.")
        else:
            print(f"Field with name '{field_name}' already exists.")

    def edit_field(self, field_name, action, culture_name=None, area=None, work_schedule=None, new_work_schedule=None, new_area=None):
        if field_name in self.fields:
            field = self.fields[field_name]
            if action == "plant":
                field.plant_crops(culture_name, area)
            elif action == "remove":
                field.remove_crops(culture_name)
            elif action == "schedule":
                field.create_work_schedule(culture_name, work_schedule)
            elif action == "edit_schedule" and isinstance(field, CultivatedField):
                field.edit_work_schedule(culture_name, new_work_schedule)
            elif action == "delete_schedule" and isinstance(field, CultivatedField):
                field.delete_work_schedule(culture_name)
            elif action == "edit_area":
                planner.fields[field_name].edit_culture_area(culture_name, new_area)
            else:
                print("Invalid action.")
        else:
            print(f"Field with name '{field_name}' does not exist.")

    def display_all_fields_info(self):
        for field in self.fields.values():
            field.display_info()

    def display_work_schedules(self):
        for field in self.fields.values():
            if isinstance(field, CultivatedField) and field.work_schedule:
                print(f"\nWork Schedules for Field '{field.field_name}':")
                for culture, work_schedule in field.work_schedule.items():
                    print(f"  - Culture: {culture}")
                    print(f"    Work Schedule: {', '.join(work_schedule.keys())}")
        print()


# Запуск програми
planner = FarmPlanner()

while True:
    print("\n1. Create Field")
    print("2. Plant Crops")
    print("3. Remove Crops")
    print("4. Create Work Schedule")
    print("5. Edit Work Schedule")
    print("6. Delete Work Schedule")
    print("7. Display Field Information")
    print("8. Display All Fields Information")
    print("9. Display all schedules and plans")
    print("10. Edit crop area")
    print ("11. Exit")
    choice = input("Enter your choice: ")

    if choice == "11":
        print("Exiting the program.")
        break

    if choice == "1":
        field_name = input("Enter field name: ")
        area_size = float(input("Enter field area size in hectares: "))
        cultivated = input("Is the field cultivated? (yes/no): ").lower() == "yes"
        planner.create_field(field_name, area_size, cultivated)
    elif choice in ["2", "3", "4", "5", "6"]:
        field_name = input("Enter field name: ")
        action = "plant" if choice == "2" else "remove" if choice == "3" else "schedule" if choice == "4" else \
            "edit_schedule" if choice == "5" else "delete_schedule"
        if action == "plant" or action == "remove":
            culture_name = input("Enter culture name: ")
            area = float(input("Enter area in hectares: "))
            planner.edit_field(field_name, action, culture_name, area)
        elif action == "schedule":
            culture_name = input("Enter culture name: ")
            work_schedule = input("Enter work schedule (comma-separated): ").split(', ')
            planner.edit_field(field_name, action, culture_name, work_schedule)
        elif action == "edit_schedule" or action == "delete_schedule":
            if action == "edit_schedule":
                new_work_schedule = input("Enter new work schedule (comma-separated): ").split(', ')
            else:
                new_work_schedule = None
            culture_name = input("Enter culture name: ")
            planner.edit_field(field_name, action, culture_name, new_work_schedule=new_work_schedule)
    elif choice == "7":
        field_name = input("Enter field name: ")
        planner.fields[field_name].display_info()
    elif choice == "8":
        planner.display_all_fields_info()
    elif choice == "9":
        planner.display_work_schedules()
    elif choice == "10":
        field_name = input("Enter field name: ")
        culture_name = input("Enter culture name: ")
        new_area = float(input("Enter new area in hectares: "))
        planner.edit_field(field_name, "edit_area", culture_name, new_area=new_area)

    else:
        print("Invalid choice. Please enter a valid option.")
