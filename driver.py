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
    for parent in driver.find_elements_by_css_selector("h2"):
        for child in parent.find_elements_by_tag_name("a"):
            theLink = child.get_attribute("href")
            lastLink = str(theLink)
            print lastLink
            if lastLink != None and parent.text != '':
                name_string = parent.text.split(" ")
                new_dict = {
                    'firstname': name_string[0],
                    'lastname': name_string[1],
                    'linkedin': lastLink
                }
                leaders.append(new_dict)
    if len(leaders) >= 8:
        removed = leaders.pop()

# def getBetterCloudList():
#     for parent in driver.find_elements_by_css_selector("#leaders > div > div:nth-child(2)"):
#         for child in parent.find_elements_by_css_selector("h2.style-title"):
#             if parent.text != '':
#                 name_string = child.text.split(" ")
#                 new_dict = {
#                     'firstname': name_string[0],
#                     'lastname': name_string[1]
#                 }
#                 leaders.append(new_dict)
#     print leaders


def getBetterCloudNames():
    for parent in driver.find_elements_by_css_selector("#leaders > div > div:nth-child(2)"):
        for child in parent.find_elements_by_tag_name("h2"):
            print child.text
# Get leaders title
def getBetterCloudTitle():
    parent = driver.find_elements_by_css_selector("#leaders > div:nth-child(1) > div:nth-child(2)")[0]
    index = 0
    for child in parent.find_elements_by_tag_name("h5"):
        leaders[index]['title'] = child.text
        index += 1

# def getBetterCloudNameCount():
#     parent = driver.find_elements_by_css_selector("#leaders > div")[0]
#     for child in parent.find_elements_by_tag_name("div"):
#             for name in leaders:
#                 leader_name_count = 0
#                 index = 0
#                 leader_first_name = name['firstname']
#                 leader_last_name = name ['lastname']
#                 print "This is the current leader %s" % leader_first_name
#                 for grandchild in child.find_elements_by_tag_name("p"):
#                     string = grandchild.text.upper()
#                     the_list = string.split()
#                     firstname_count = the_list.count(name['firstname'])
#                     print the_list
#                     lastname_count = the_list.count(name['lastname'])
#                     leader_name_count = firstname_count - lastname_count
#                 leaders[index]['name_count'] = leader_name_count
#                 index += 1
#                 leader_name_count = 0


def getBetterCloudNameCount():
    div_index = 1
    selector = "#leaders > div > div:nth-child(2) > div:nth-child(%d)" % div_index
    parent = driver.find_elements_by_css_selector(selector)[0]
    index = 0
    for name in leaders:
        leader_name_count = 0
        leader_first_name = name['firstname']
        leader_last_name = name ['lastname']
        for child in parent.find_elements_by_tag_name("p"):
            string = child.text.upper()
            the_list = string.split()
            firstname_count = the_list.count(name['firstname'])
            print the_list
            lastname_count = the_list.count(name['lastname'])
            leader_name_count = firstname_count - lastname_count
        leaders[index]['name_count'] = leader_name_count
        leader_name_count = 0
        index += 1
    div_index += 2
# morgan@notion
getBetterCloudList()
getBetterCloudLeaderImage()
getBetterCloudTitle()
getBetterCloudNameCount()
for leader in leaders:
    print leader
    print leader['firstname']
    print leader['lastname']
    # print leader['linkedin']
    # print leader['image_url']
    # print leader['title']
    # print leader['name_count']


driver.quit()
