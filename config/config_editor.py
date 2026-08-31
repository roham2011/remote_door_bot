import json

# ============================================================
# edit config function
# ============================================================
def edit_config(settings_path):
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
        debug_choice = input("Select debug state [1] True [2] False: ").strip()

        if debug_choice == "1":
            debug = True
            break

        elif debug_choice == "2":
            debug = False
            break

        else:
            print("Invalid debug selection.")

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
        "num_of_doors": num_of_doors
    }

    # Save configuration
    with open(settings_path, "w") as file:
        json.dump(config, file, indent=4)

    print("\nConfiguration saved successfully.")

    return config


