import json
from configs.path import SETTINGS_PATH

# ============================================================
# edit config function
# ============================================================
def edit_config():
    print("\n" + "=" * 70)
    print("configuration")
    print("=" * 70)

    print("No configuration file was found.\n")

    # PORT
    while True:
        try:
            app_port = int(input("Enter Flask port: "))
            if 1 <= app_port <= 65535:
                break

            print("Port must be between 1 and 65535.")

        except ValueError:
            print("Port must be a number.")

    # NUMBER OF DOORS
    while True:
        try:
            num_of_doors = int(input("Enter number of doors: "))

            if num_of_doors >= 1:
                break

            print("Number of doors must be at least 1.")

        except ValueError:
            print("Number of doors must be a number.")

    # HOST
    host = input("Enter Flask host [127.0.0.1]: ").strip()

    if not host:
        host = "127.0.0.1"

    # DEBUG
    while True:
        debug_choice = input(
            "Select debug state [1] True [2] False: "
        ).strip()

        if debug_choice == "1":
            debug = True
            break

        elif debug_choice == "2":
            debug = False
            break

        else:
            print("Invalid debug selection.")

    # ROOT ADMIN
    while True:
        try:
            root_admin = int(input("Enter Root Admin Bale User ID: "))

            if root_admin > 0:
                break

            print("Bale User ID must be greater than 0.")

        except ValueError:
            print("Bale User ID must be a number.")
            
    # TOKEN
    while True:
        token = input("Enter Bale Bot token: ").strip()

        if token:
            break

        print("Token cannot be empty.")

    # Build configuration
    config = {
        "app_port": app_port,
        "debug": debug,
        "host": host,
        "token": token,
        "num_of_doors": num_of_doors,
        "admins": [
            root_admin
        ]
    }

    # Save configuration
    with open(SETTINGS_PATH, "w") as file:
        json.dump(config, file, indent=4)

    print("\nConfiguration saved successfully.")

    return config