from requests import get as rget
import time
import os

proxySwap = False

def get_asset(asset_id):
    while True:
        global proxySwap

        if proxySwap == True:
            response = rget(f"https://economy.roblox.com/v2/assets/{asset_id}/details")
        else:
            response = rget(f"https://economy.roproxy.com/v2/assets/{asset_id}/details")
        
        if response.status_code == 200:
            asset_info = response.json()
            creator_name, asset_name = asset_info.get("Creator").get("Name"), asset_info.get("Name")
            if creator_name and asset_name:
                return creator_name, asset_name
        elif response.status_code == 400:
                break
        elif response.status_code == 429:
            proxySwap = not proxySwap
            time.sleep(0.1)

def confirm_asset(current_id, asset_owners):
    
    try:
        owner, asset_name = get_asset(current_id)
    except Exception:
        return # Skip

    if owner == None:
        return # Skip
    
    if asset_name == None:
        return # Skip

    if not owner in asset_owners:
        return # Skip
    
    # Write

    print(f"{asset_name} | {current_id} | {owner}")

    try:
        f = open("assets.txt", "x")
    except FileExistsError:
        print("assets.txt already exists")
        with open("assets.txt", "w") as f:
            f.write("")

    with open("assets.txt", "a") as f:
        f.write(f"\n{asset_name} | {current_id} | {owner}")

def main():
    while True:
        start_id = input("Starting asset ID: ")
        if start_id.isnumeric():
            break
        else:
            print("Must be a number")
    while True:
        ending_id = input("Ending asset ID (put 0 for no end): ")
        if ending_id.isnumeric():
            break
        else:
            print("Must be a number")

    current_id = int(start_id)
    ending_id = int(ending_id)
    
    asset_owners_input = input("Enter owner IDs (comma-separated, e.g., 123,456,789): ")
    asset_owners = asset_owners_input.split(",")

    if ending_id == 0:
        ending_id = float("inf")

    print(
        f"Starting scanning from ID {start_id} and ending at {ending_id}"
        )

    while True:
        if current_id > (ending_id):
            break
        confirm_asset(current_id, asset_owners)
        current_id += 1
        time.sleep(0.3)

if __name__ == "__main__":
    main()
