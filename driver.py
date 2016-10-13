import os
import sys
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# I was working inside a python virtual env during this project
# Create a new instance of the Firefox driver. I spent a good deal of time trouble shooting Firefox driver problems and was finally able to make it work by using an older version of FireFox(46.0.1).
driver = webdriver.Firefox()

# Navigate to BetterCloud
driver.get("https://www.bettercloud.com/about-us")

# Navigate to LeaderShip page
leadershp_link = driver.find_element_by_link_text("LEADERSHIP")
leadershp_link.click()

# Make sure page has loaded after leadership link is clicked. I spent a good amount with this. Many of the articles I read told me this was unnecessary with newer version of selenium. However, when I would select the leadership tab, the data would sometimes not be there. My assumption was that my python was running before javascript had completely updated the DOM since I was navigating after the page had loaded. This seems to have fixed the problem and my functions run as expected.
try:
    element = WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.XPATH, "//*[@id='leaders']/div/div[2]/div[1]/h2"), 'DAVID POLITIS'))
finally:

# I initially just built functions to get each piece of data by leader location alone. I only wanted to use one main selector and then have that code be reran for each leader given only there location. This seemed logical in that each leaders html was structured the same with each having there own div. I then refactored into a Leader class in order to reduce the amount of duplicated code.
    class Leader(object):
        def __init__(self, location):
            self.location = location
            self.parent = driver.find_element_by_xpath(self.location)

        # Class method to return the name of the leader at given location
        def getBetterCloudName(self):
            for child in self.parent.find_elements_by_xpath("./h2"):
                name_string = child.text
                return name_string

        # Class method to return the title of the leader at given location
        def getBetterCloudTitle(self):
            for child in self.parent.find_elements_by_xpath("./h5"):
                return child.text

        # Class method to return the image url of leader at given location
        def getBetterCloudLeaderImage(self):
            for child in self.parent.find_elements_by_tag_name("img"):
                the_image = child.get_attribute("src")
                if "icon" not in the_image:
                    return the_image

        # Class method to return the LinkedIn url of leader at given location
        def getBetterCloudLinkedIn(self):
            for child in self.parent.find_elements_by_xpath("./h2/a"):
                theLink = child.get_attribute("href")
                lastLink = str(theLink)
                return lastLink

        # Class method to return the name count of leader at given location excluding full name entries
        def getBetterCloudNameCount(self, name):
            name = name.split()
            firstname = name[0]
            lastname = name[1]
            leader_name_count = 0
            for child in self.parent.find_elements_by_tag_name("p"):
                string = child.text.upper()
                string_array = string.split()
                # This was my first attempt at solving the name count problem and it was working until I ran it using Russell Sachs location where they referrence him by last name instead of his first.
                # firstname_count = string_array.count(firstname)
                # lastname_count = string_array.count(lastname)
                # leader_child_name_count = firstname_count - lastname_count
                # leader_name_count += leader_child_name_count

                # Second solution to name count problem and overall it is a more thorough and eloquent solution
                for index, item in enumerate(string_array):
                    next = index + 1
                    if item == firstname and string_array[next] != lastname:
                        leader_name_count += 1

            return leader_name_count

        def getLinkedInInformation(self, url, logged_in):
            for child in self.parent.find_elements_by_tag_name("a"):
                if child.get_attribute("href") == url:
                    link = child
            # I struggled to get the link to click and the problem appeared to be with the image covering the link. Not 100%, but this was a workable solution to the problem.
            driver.execute_script("arguments[0].click();", link)
            for handle in driver.window_handles:
                driver.switch_to.window(handle)
            # I ran into a problem when selenium click the linkedIn link for the first time, I was not logged in to LinkedIn. I would then log in and switch the logged_in variable to True so that I would not repeat the process after the initial log in. The instuctions said to click the links. Another solution would be to follow each link that I have stored so selenium isnt opening new browsers for each link. To test this, a username and password will need to be entered as I do not wish to give out my password for linkedin.
            if logged_in == False:
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "sign-in-link")))
                finally:
                    link = driver.find_element_by_link_text("Sign in")
                    link.click()
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "btn-primary")))
                finally:
                    email_input = driver.find_element_by_name("session_key")
                    # Input linkedin email address to test this.
                    email_input.send_keys('email)
                    password_input = driver.find_element_by_name("session_password")
                    # Input linkedin pasword to test this.
                    password_input.send_keys('password')
                    submit = driver.find_element_by_name('signin')
                    submit.click()
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "full-name")))
            finally:
                for location in driver.find_elements_by_xpath("//*[@id='location']/dl/dd[1]/span/a"):
                    local = location.text
                for education in driver.find_elements_by_xpath("//*[@id='overview-summary-education']/td/ol/li/a"):
                    edu = education.text
                driver.switch_to.window(driver.window_handles[0])
                return [local, edu]

        # Class method that calls the other methods and return a dictionary for leader at given location
        def buildLeaderDictionary(self, logged_in):
            name = self.getBetterCloudName()
            title = self.getBetterCloudTitle()
            image = self.getBetterCloudLeaderImage()
            Linkedin = self.getBetterCloudLinkedIn()
            count = self.getBetterCloudNameCount(name)
            linked_in_info = self.getLinkedInInformation(Linkedin, logged_in)
            split_name = name.split()
            firstname = split_name[0]
            lastname = split_name[1]
            new_dict = {
            'firstname': firstname,
            'lastname': lastname,
            'title': title,
            'image_url': image,
            'linkedin': Linkedin,
            'name_count': count,
            'location': linked_in_info[0],
            'education': linked_in_info[1]
            }
            return new_dict


    leaders = []
    def getLeaders():
        # Xpath location of each leader on the bettercloud about us web page.
        leader_location = ["//*[@id='leaders']/div/div[2]/div[1]","//*[@id='leaders']/div/div[2]/div[2]","//*[@id='leaders']/div/div[2]/div[3]","//*[@id='leaders']/div/div[2]/div[4]","//*[@id='leaders']/div/div[2]/div[5]","//*[@id='leaders']/div/div[2]/div[6]","//*[@id='leaders']/div/div[2]/div[7]"]

        # The logged_in variable is passed when the buildLeaderDictionary function is called so that the log in process is only attempted once.
        logged_in = False
        for leader in leader_location:
            the_leader = Leader(leader).buildLeaderDictionary(logged_in)
            leaders.append(the_leader)
            logged_in = True
            print the_leader
    # Writes data to the csv file leaders.csv
    def writeLeaderData():
        with open('leaders.csv', "wb") as csvfile:
            write = csv.writer(csvfile, delimiter = ' ')
            for leader in leaders:
                write.writerow(["Title:", leader['title']])
                write.writerow(["First Name:", leader['firstname']])
                write.writerow(["Last Name:", leader['lastname']])
                write.writerow(["Location:", leader['location']])
                write.writerow(["Education:", leader['education']])
                write.writerow(["Name count:", leader['name_count']])
                write.writerow(["LinkedIn:", leader['linkedin']])
                write.writerow(["Image url:", leader['image_url']])
                write.writerow(["# - - - - - - - - - - - - - - #"])

    getLeaders()
    writeLeaderData()
    driver.quit()
