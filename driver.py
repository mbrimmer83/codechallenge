from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        # Class method to return the name count of leader at given location
        def getBetterCloudNameCount(self, name):
            name = name.split()
            firstname = name[0]
            lastname = name[1]
            leader_name_count = 0
            for child in self.parent.find_elements_by_tag_name("p"):
                string = child.text.upper()
                string_array = string.split()
                firstname_count = string_array.count(firstname)
                lastname_count = string_array.count(lastname)
                leader_child_name_count = firstname_count - lastname_count
                leader_name_count += leader_child_name_count
            return leader_name_count

        # Class method that calls the other methods and return a dictionary for leader at given location
        def buildLeaderDictionary(self):
            name = self.getBetterCloudName()
            title = self.getBetterCloudTitle()
            image = self.getBetterCloudLeaderImage()
            Linkedin = self.getBetterCloudLinkedIn()
            count = self.getBetterCloudNameCount(name)
            split_name = name.split()
            firstname = split_name[0]
            lastname = split_name[1]
            new_dict = {
            'firstname': firstname,
            'lastname': lastname,
            'title': title,
            'image_url': image,
            'linkedin': Linkedin,
            'name_count': count
            }
            return new_dict


    leader_location = ["//*[@id='leaders']/div/div[2]/div[1]","//*[@id='leaders']/div/div[2]/div[2]","//*[@id='leaders']/div/div[2]/div[3]","//*[@id='leaders']/div/div[2]/div[4]","//*[@id='leaders']/div/div[2]/div[5]","//*[@id='leaders']/div/div[2]/div[6]","//*[@id='leaders']/div/div[2]/div[7]"]
    leaders = []
    for leader in leader_location:
        the_leader = Leader(leader).buildLeaderDictionary()
        leaders.append(the_leader)
        print the_leader
    driver.quit()
