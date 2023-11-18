from core.iterate import iterating, get_api_key

def main():
    # Get api key if not already gotten.
    get_api_key()

    # Build software
    print("Building the requested software...")
    is_iterating = iterating()
    while is_iterating:
        is_iterating = iterating()
    
    print("Done.")



if __name__ == "__main__":
    main()