import requests
import time
import random
import string
from colorama import Fore, Style, init

init()

VOWELS = set('aeiou')
CONSONANTS = set(string.ascii_lowercase) - VOWELS

def generate_pronounceable_username(length=5):
    """Generate a pronounceable username directly instead of trial and error."""
    username = []
    # Start randomly with vowel or consonant
    is_vowel_next = random.choice([True, False])
    
    for _ in range(length):
        # Select from appropriate letter pool
        if is_vowel_next:
            letter = random.choice(list(VOWELS))
        else:
            letter = random.choice(list(CONSONANTS))
            
        # Ensure no three consecutive same letters
        if len(username) >= 2 and username[-1] == username[-2] == letter:
            # Try a different letter from the same group
            available_letters = (VOWELS if is_vowel_next else CONSONANTS) - {letter}
            letter = random.choice(list(available_letters))
            
        username.append(letter)
        is_vowel_next = not is_vowel_next  # Alternate between vowel and consonant
    
    return ''.join(username)

def generate_random_username(length=5):
    """Generate a completely random username."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def check_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?Username={username}&Birthday=2000-01-01"
    try:
        response = requests.get(url)
        
        if response.status_code == 429:
            print(Fore.YELLOW + "Rate-limited by the server. Stopping the script." + Style.RESET_ALL)
            print("Response text:", response.text)
            return False

        response_data = response.json()
        code = response_data.get("code")
        
        if code == 0:
            print(Fore.GREEN + f"VALID: {username}" + Style.RESET_ALL)
            with open("valid_usernames.txt", "a") as valid_file:
                valid_file.write(username + "\n")
        elif code == 1:
            print(Fore.LIGHTBLACK_EX + f"TAKEN: {username}" + Style.RESET_ALL)
        elif code == 2:
            print(Fore.RED + f"CENSORED: {username}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + f"bruh ({code}): {username}" + Style.RESET_ALL)

    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"glitch {username}: {e}" + Style.RESET_ALL)
    
    return True

def main():
    # Get desired length
    while True:
        try:
            length = int(input("Enter desired username length (3-20): "))
            if 3 <= length <= 20:
                break
            else:
                print(Fore.RED + "Username length must be between 3 and 20 characters!" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Please enter a valid number!" + Style.RESET_ALL)
    
    # Get generation method preference
    while True:
        choice = input("Pronounceable username only? (y/n): ").lower()
        if choice in ['y', 'n']:
            break
        print(Fore.RED + "Please enter 'y' for yes or 'n' for no!" + Style.RESET_ALL)

    while True:
        if choice == 'y':
            username = generate_pronounceable_username(length)
        else:
            username = generate_random_username(length)
            
        if not check_username(username):
            break
        time.sleep(0.05)

if __name__ == "__main__":
    main()