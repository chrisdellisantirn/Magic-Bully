from pyfiglet import Figlet
from collections import Counter
from datetime import datetime
from numpy import *
import requests, sys

def main():
    banner()
    response = get_api("https://data.ny.gov/resource/d6yy-54nr.json")
    white_balls, red_balls = get_numbers(response)
    white, red = count_sort(white_balls, red_balls)
    color, lucky_num = get_lucky()
    picks = generate_picks(white, red, color, lucky_num)
    with open('powerball_picks.txt', 'a+') as file:
        file.write(f"Magic Bully Powerball Picks!\n")
        for item in picks:
            file.write(f"{item}\n")
        file.write(f"\n")

def banner():
    font = Figlet(font="small")
    print(font.renderText("Magic Bully"))

def get_api(api):
    try:
        r = requests.get(api)
        data = r.json()
        return data
    except (requests.RequestException, requests.exceptions.JSONDecodeError):
        sys.exit('Failed to retrieve API')

def get_numbers(json):
    winning_nums = []
    for key in json:
        if datetime.fromisoformat(key['draw_date']) > datetime.fromisoformat('2015-10-03'):
            winning_nums.append(key['winning_numbers'].split())
    white_balls = []
    for balls in winning_nums:
        for ball in balls[:5]:
            white_balls.append(int(ball))
    red_balls = []
    for powerball in winning_nums:
        red_balls.append(int(powerball[5]))
    return white_balls, red_balls

def count_sort(n, n2):
    dict_n = Counter(n)
    dict_n2 = Counter(n2)
    return dict_n.most_common(), dict_n2.most_common()

def get_lucky():
    while True:
        response = input('🍀 Want to play a lucky number? (Y/N): ').casefold().strip()
        if response == 'y':
            ball = input('Should your number be a white ball or the Powerball? (white/red): ').casefold().strip()
            if ball == 'white':
                print('⚪ Pick a number between 1-69')
                lucky_white = int(input('Lucky number: '))
                if lucky_white in range (1,70):
                    return 'white', lucky_white
                else:
                    print('Invalid entry')
                    continue
            elif ball == 'red':
                print('🔴 Pick a number between 1-26')
                lucky_red = int(input('Lucky number: '))
                if lucky_red in range(1,27):
                    return 'red', lucky_red
                else:
                    print('Invalid entry')
                    continue
            else:
                print('Invalid entry')
                continue
        elif response == 'n':
            return None, None
        else:
            print('Invalid entry')
            continue

def generate_picks(white, red, color, lucky_number):
    white_probs = []
    white_balls = []
    white_freq = []
    for k,v in white:
        white_balls.append(k)
        white_freq.append(v)
    for wf in white_freq:
        white_prob = wf / sum(white_freq)
        white_probs.append(white_prob)

    red_probs = []
    red_balls = []
    red_freq = []
    for k,v in red:
        red_balls.append(k)
        red_freq.append(v)
    for rf in red_freq:
        red_prob = rf / sum(red_freq)
        red_probs.append(red_prob)
    
    picks = []
    ln = [lucky_number]
    if color == 'white':
        for _ in range(5):
            wb = array(random.choice(white_balls, 4, replace=False, p=white_probs)).tolist()
            rb = array(random.choice(red_balls, 1, replace=False, p=red_probs)).tolist()
            swb = wb.sort()
            picks.append(f"{ln + swb}{rb}")
        return(picks)
    elif color == 'red':
        for _ in range(5):
            wb = array(random.choice(white_balls, 5, replace=False, p=white_probs)).tolist()
            swb = wb.sort()
            picks.append(f"{wb}{ln}")
        return(picks)
    else:
        for _ in range(5):
            wb = array(random.choice(white_balls, 5, replace=False, p=white_probs)).tolist()
            rb = array(random.choice(red_balls, 1, replace=False, p=red_probs)).tolist()
            swb = wb.sort()
            picks.append(f"{wb}{rb}")
        return(picks)

if __name__ == '__main__':
    main()