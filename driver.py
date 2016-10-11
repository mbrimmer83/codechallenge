from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# Create a new instance of the Firefox driver
driver = webdriver.Firefox()

# Navigate to BetterCloud
driver.get("https://www.bettercloud.com/about-us ")
print driver.title

# Navigate to LeaderShip page
leadershp_link = driver.find_element_by_link_text("LEADERSHIP")
leadershp_link.click()
# Leaders list of dictionaries
leaders = []

# Get leaders image url
def getBetterCloudLeaderImage():
    parent = driver.find_elements_by_css_selector("#leaders > div:nth-child(1) > div:nth-child(2)")[0]
    index = 0
    image = parent.find_elements_by_tag_name('img')
    for child in image:
        the_image = child.get_attribute("src")
        last_image = the_image
        if "icon" not in last_image:
            leaders[index]['image_url'] = last_image
            index += 1

# Get leaders names and linkedin url
def getBetterCloudList():
    for parent in driver.find_elements_by_css_selector("h2.style-title"):
        for child in parent.find_elements_by_tag_name("a"):
            theLink = child.get_attribute("href")
            lastLink = str(theLink)
            if lastLink != None and parent.text != '':
                name_string = parent.text.split(" ")
                new_dict = {
                    'firstname': name_string[0],
                    'lastname': name_string[1],
                    'linkedin': lastLink
                }
                leaders.append(new_dict)

# Get leaders title
def getBetterCloudTitle():
    parent = driver.find_elements_by_css_selector("#leaders > div:nth-child(1) > div:nth-child(2)")[0]
    index = 0
    for child in parent.find_elements_by_tag_name("h5"):
        leaders[index]['title'] = child.text
        index += 1

def getBetterCloudNameCount():
    for parent in driver.find_elements_by_css_selector("#leaders > div"):
        index = 0
        leader_string = ""
        child = parent.find_elements_by_tag_name("p")
        for idx in child:
            string = str(idx)
            if leaders[index]['firstname'] in string:
                leader_string = leader_string + string
            elif leaders[index + 1]['firstname'] in string:
                print leader_string
                leaders[index]['leader_text'] = leader_string
                leader_string = ""
                leader_string = leader_string + string
                index += 1
            else:
                pass




getBetterCloudList()
getBetterCloudLeaderImage()
getBetterCloudTitle()
getBetterCloudNameCount()
for leader in leaders:
    print leader['firstname']
    print leader['lastname']
    print leader['linkedin']
    print leader['image_url']
    print leader['title']


driver.quit()
