### Recursively download webcomics from newest to oldest.

# TODO: I don't think anything? Works like I want.

from selenium import webdriver
import bs4, os, requests, webbrowser, shutil

# VARIABLES:
# folder | start_url | comic_container | back_button  | naming_convention
# choice | comic_url | comic_name

#####################################################

folder = r''
start_url = r''
comic_container = r''
back_button = r''
naming_convention = r''
choice = 0
comic_url = r''
comic_name = r''

### GETTING USER INFO ###

# Request the folder the user would like to save to.
folder = input(r'Where are we saving the images? ')
os.chdir(folder) # Change our working directory to the specified folder.

# Check to see if we have chromedriver.exe in the folder (for navigating the site).
for root, dirs, files in os.walk(folder):
    if os.path.isfile('chromedriver.exe') == True:
        break
    else: # If we don't, we'll copy the version that's in my Code directory.
        shutil.copy(r'C:\Users\PhooM\Desktop\Code\Scripts\Python\chromedriver.exe', folder)

# Request the site's URL on the page you want to start.
start_url = input(r'What page are we starting on? ')

# Grab our CSS selectors for both the comic's container and the back button.
comic_container = input(r'What is the CSS selector for the comic? ')
back_button = input(r'What is the CSS selector for the back button? ')

# Are we basing the naming convention off of the URL or by file name?
print(r'Are we using the URL or file name as naming convention? ')
print(r'Type URL or File')
naming_convention = input(r'> ')

# Make sure the user typed one of our two choices properly.
if naming_convention.lower() == 'file':
    choice = 0
elif naming_convention.lower() == 'url':
    choice = 1
else:
    print(r'You must enter URL or File.')

comic_name = input(r'How would you like the filename to start? ')

#####################################################

# Open a browser window and navigate to the user's specified page.
# We need to do this outside of the loop the first time to get started,
# but the loop will take care of the rest.
browser = webdriver.Chrome()
browser.get(start_url)

while True:
    try:
        # Snag the page's URL.        
        start_url = browser.current_url

        # Slap together a Beautiful Soup object for the current page.
        res = requests.get(start_url)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Set our selectors based on previously acquired info.
        comic = browser.find_element_by_css_selector(comic_container)
        back = browser.find_element_by_css_selector(back_button)

        ## We find the first image, which should be the comic.
        #images = soup.find('a > img')

        comic_url = comic.get_attribute('src')

        print('We got the comic URL.')
    
        # Process how we're going to name these files.
        if choice == 0:
            name = comic_url.split('/')[-1]
        else:
            # If the user wants to use the URL for naming...
            name = start_url.split('/')[-1]

        print('We have got the naming convention.')

        # Create a response object for the comic file's URL.
        response = requests.get(comic_url)

        print('We have gotten the response object.')

        # Actually save the file in our provided directory.
        with open(comic_name + '-' + name, 'wb') as f:
            f.write(response.content)

        # Go to previous page so we can keep the downloads rollin'.
        back.click()

        continue
        
    except Exception as e:
        print(e)
