import os
import spotipy
import time
import subprocess
import pygetwindow as gw
from subprocess import Popen
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from pynput.keyboard import Key, Controller




def display_menu():
    print('SPOTIFY DESKTOP AD SKIP - WINDOWS')
    print('1: Block Ads')
    print('2: Change Directory Path for Spotify Desktop App')
    print('3: Exit\n')


def get_user_win():
    resolution = False
    while(not resolution):
        try:
            user_win = gw.getActiveWindow()
            if (user_win):
                resolution = True
        except Exception as e:
            time.sleep(.25)
            print('Get user_win error:' + str(e))
    return user_win

def get_track_info(sp):
    resolution = False
    while(not resolution): #this loops when program enters blockads function and spotify player is not playing
        try:
            track_info = sp.current_user_playing_track()
            if(track_info):
                resolution = True
            else:
                time.sleep(2)
        except Exception as e:
            print(e)
            time.sleep(2)
    print("Spotify API call successful.")
    return track_info


def restart_spotify(path):
    try:
        subprocess.call(['taskkill','/F','/IM','Spotify.exe'])
    except:
        pass
    time.sleep(.5)
    try:
        if os.path.isfile(path):
            subprocess.Popen(path, shell=True)
        else:
            print('\nDirectory path entered does not exist! \nRe-enter the correct directory path from the main menu.')
            time.sleep(5)
            return False
    except Exception as e:
        print(e)
        return False
    win = gw.getWindowsWithTitle('Spotify Free')
    if win != []:
        try:
            win[0].activate()
        except:
            win[0].minimize()
            win[0].restore()
    time.sleep(.75)
    return True


def press_play(pynput_keyboard):
    pynput_keyboard.press(Key.space)
    pynput_keyboard.release(Key.space)
    time.sleep(.1)


def next_track(pynput_keyboard):
    pynput_keyboard.press(Key.ctrl)
    pynput_keyboard.press(Key.right)
    pynput_keyboard.release(Key.ctrl)
    pynput_keyboard.release(Key.right)
    time.sleep(.1)


def restore_user_window(pynput_keyboard):
    pynput_keyboard.press(Key.alt_l)
    pynput_keyboard.press(Key.tab)
    pynput_keyboard.release(Key.alt_l)
    pynput_keyboard.release(Key.tab)
    time.sleep(.1)





def block_ads(pynput_keyboard, sp, path):
    s = subprocess.check_output('tasklist', shell=True)
    spotify_win = None
    if "Spotify.exe" in str(s):
        running = restart_spotify(path)
        if(running):
            spotify_win = get_user_win()
            current = get_track_info(sp) # this is a dictionary that contains information about current track playing
            if(current['is_playing']):
                press_play(pynput_keyboard)
            print(spotify_win)
    else:
        print('\nSpotify Desktop App is not running. Open the app and try again.')
        time.sleep(3)
        running = False

    while(running):
        time.sleep(.75)
        current = get_track_info(sp) # this is a dictionary that contains information about current track playing
        if(current and current['currently_playing_type'] != 'ad'):

            try:
                print("Currently playing as of last API call: " + current['item']['album']['artists'][0]['name'] + ' - ' + current['item']['name'])
                print('Spotify Window Title: ' + str(spotify_win.title))
            except:
                pass
            user_win = get_user_win()
            print('Active Window Title: ' + str(user_win.title))

        s = subprocess.check_output('tasklist', shell=True)
        if(not("Spotify.exe" in str(s))):
            running = False

        if(running and current['is_playing']):
            if(current['currently_playing_type'] == 'ad'):
                user_win = get_user_win()
                running = restart_spotify(path)
                spotify_win = get_user_win()
                press_play(pynput_keyboard)
                next_track(pynput_keyboard)
                if(user_win != spotify_win):
                    restore_user_window(pynput_keyboard)
                print('ad closed')
                time.sleep(.25)

            elif(current['currently_playing_type'] != 'ad'):
                waiting = True
                start = time.time()
                end = time.time()
                try:
                    while(waiting and end - start < current['item']['duration_ms'] - current['progress_ms']):
                        end = time.time()
                        if(current['item']['album']['artists'][0]['name'] + ' - ' + current['item']['name'] != spotify_win.title):
                            waiting = False
                except: 
                    pass
                
        else:
            if "Spotify.exe" in str(s):
                try: #if Spotify player is paused.
                    win = gw.getWindowsWithTitle('Spotify Free')
                    while(True):
                        win = gw.getWindowsWithTitle('Spotify Free')
                        if win == []:
                            break
                except Exception as e: #Spotify player is not paused, Retry API call
                    print(e)
                    time.sleep(.5)
            else:
                print('\nSpotify Desktop App is not running. Open the app and try again.')
                time.sleep(3)
                running = False        


def main():
    load_dotenv()
    pynput_keyboard = Controller()
    
    scope = "user-read-currently-playing"
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, requests_timeout=5))
    except Exception as e:
        print(e)
        exit(1)
    run_app = True
    option = 0
    while (run_app):
        display_menu()
        option = int(input('Enter: '))
        if(option == 1):
            try:
                path_file = open('path.txt', 'r')
                path = path_file.read()
                if(path == ''):
                    raise Exception
            except:
                path_file = open('path.txt', 'w')
                path = str(input('Enter the directory path of the Spotify desktop application: '))
                path_file.write(path)
            path_file.close()
            block_ads(pynput_keyboard, sp, path)
        elif(option == 2):
            path_file = open('path.txt', 'w')
            path = str(input('Enter the directory path of the Spotify desktop application: '))
            path_file.write(path)
            path_file.close()
        else:
            run_app = False
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':        
    main()
        

            
