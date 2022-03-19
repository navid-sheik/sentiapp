from django.test import TestCase


from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.contenttypes.models import ContentType
from selenium.webdriver.common.by import By


from selenium import webdriver

from django.urls import reverse,resolve
from singleticker.views import singleStockView

import time


# class TestMining(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         ContentType.objects.clear_cache
#         super().setUpClass()
#         cls.driver =  webdriver.Chrome()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.driver.quit()
#         super().tearDownClass()

#     def setUp(self) -> None:
   
#         return super().setUp()
#     def test_start_mining(self):
#         driver =  self.driver
#         url =  self.live_server_url + reverse("home:home")
#         driver.get(url)
#         time.sleep(10)
#         driver.find_element_by_id('mine-btn-ATVI').click()
#         time.sleep(10)
#         #click the first button with mine 

#         text  =  driver.find_element_by_id('view-btn-ATVI').text
#         isDisplayed =  driver.find_element_by_id('view-btn-ATVI').is_displayed()
#         time.sleep(10)
#         # self.assertEqual(text , "VIEW")
#         self.assertEqual(True, isDisplayed)
#         #wait 10 seconds 

#         #check if button changed to  view 
#         #if it is passed test 
 
class TestViewStock(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ContentType.objects.clear_cache
        super().setUpClass()
        cls.driver =  webdriver.Chrome()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self) -> None:
   
        return super().setUp()
    def test_start_mining(self):
        driver =  self.driver
        url =  self.live_server_url + reverse("home:home")
        driver.get(url)
        time.sleep(10)
        driver.find_element_by_id('mine-btn-ATVI').click()
        time.sleep(10)
        #click the first button with mine 

        driver.find_element_by_id('view-btn-ATVI').click()
        time.sleep(10)
        #click a button containing the view 
        current_url= driver.current_url
        #wait 5 seconds 
        # Click the link to activate the alert
driver.find_element(By.LINK_TEXT, "See an example alert").click()

# Wait for the alert to be displayed and store it in a variable
alert = wait.until(expected_conditions.alert_is_present())

# Store the alert text in a variable
text = alert.text

# Press the OK button
alert.accept()
        print(current_url)
        #self.assertEquals(resolve(current_url).func, singleStockView)
        
        #if in another page, result passed 




# class Auth(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         ContentType.objects.clear_cache
#         super().setUpClass()
#         cls.driver =  webdriver.Chrome()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.driver.quit()
#         super().tearDownClass()

#     def setUp(self) -> None:
#         self.user_password = "queenmary"
#         self.user =  User.objects.create_user('group37', 'some@gmail.com', self.user_password)
#         self.user.profile  =  Profile(city = "London", dob='2010-12-12')
#         self.user.profile.save()
#         self.user.save()

#         return super().setUp()



#     def test_login(self):
#         driver =  self.driver
#         url =  self.live_server_url + '/login/'
#         urlRedicrect=  self.live_server_url + reverse("mainapp:profile")
#         driver.get(url)

#         username_element  =  driver.find_element_by_id('id_username')
#         username_element.clear()
#         username_element.send_keys("group37")



#         password_element =  driver.find_element_by_id('id_password')
#         password_element.clear()
#         password_element.send_keys("queenmary")

#         driver.find_element_by_xpath("//input[@type='submit']").click()
#         time.sleep(5)
#         currentUserLoggedText  =  self.driver.find_element_by_id("current_username").text

#         self.assertEqual(currentUserLoggedText, "group37")








# class Auth2(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         ContentType.objects.clear_cache
#         super().setUpClass()
#         cls.driver =  webdriver.Chrome()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.driver.quit()
#         super().tearDownClass()

#     def setUp(self) -> None:
#         self.user_password = "queenmary"
#         self.user =  User.objects.create_user('group37', 'some@gmail.com', self.user_password)
#         self.user.profile  =  Profile(city = "London", dob='2010-12-12')
#         self.user.profile.save()
#         self.user.save()

#         return super().setUp()




#     def test_signup(self):

#         driver =  self.driver
#         url =  self.live_server_url + '/register/'
#         urlRedicrect =  self.live_server_url + reverse("mainapp:profile")
#         driver.get(url)

#         username_element  =  driver.find_element_by_id('id_username')
#         username_element.clear()
#         username_element.send_keys("newtestuser")



#         password_element1 =  driver.find_element_by_id('id_password1')
#         password_element1.clear()
#         password_element1.send_keys("queenmary")


#         password_element2 =  driver.find_element_by_id('id_password2')
#         password_element2.clear()
#         password_element2.send_keys("queenmary")


#         email_element =  driver.find_element_by_id('id_email')
#         email_element.clear()
#         email_element.send_keys("sampleemail@gmail.com")




#         dob_element =  driver.find_element_by_id('id_dob')
#         dob_element.clear()
#         dob_element.send_keys("06072003")


#         city_element =  driver.find_element_by_id('id_city')
#         city_element.clear()
#         city_element.send_keys("Manchester")

#         driver.find_element_by_xpath("//input[@type='submit']").click()
#         time.sleep(5)

#         currentUserLoggedText  =  self.driver.find_element_by_id("current_username").text

#         self.assertEqual(currentUserLoggedText, "newtestuser")







# class EditProfileTest(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         ContentType.objects.clear_cache
#         super().setUpClass()
#         cls.driver =  webdriver.Chrome()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.driver.quit()
#         super().tearDownClass()

#     def setUp(self) -> None:
#         self.user_password = "queenmary"
#         self.user =  User.objects.create_user('group37', 'some@gmail.com', self.user_password)
#         self.user.profile  =  Profile(city = "London", dob='2010-12-12')
#         self.user.profile.save()
#         self.user.save()

#         return super().setUp()




#     def test_edit_profile(self):

#         driver =  self.driver
#         url =  self.live_server_url + '/login/'
#         urlRedicrect=  self.live_server_url + reverse("mainapp:profile")
#         driver.get(url)

#         username_element  =  driver.find_element_by_id('id_username')
#         username_element.clear()
#         username_element.send_keys("group37")



#         password_element =  driver.find_element_by_id('id_password')
#         password_element.clear()
#         password_element.send_keys("queenmary")

#         driver.find_element_by_xpath("//input[@type='submit']").click()

#         time.sleep(5)

#         driver.find_element_by_id("editProfileBtn").click()


#         city_element  =  driver.find_element_by_id('userCity')
#         city_element.clear()
#         city_element.send_keys("Oxford")
#         time.sleep(5)

#         driver.find_element_by_id("saveProfileBtn").click()
#         time.sleep(5)

#         currentUserCity  =  driver.find_element_by_id("profileCity").text

#         self.assertEqual(currentUserCity, "Oxford")


# class ListHobbies(StaticLiveServerTestCase):

#     @classmethod
#     def setUpClass(cls) -> None:
#         ContentType.objects.clear_cache
#         super().setUpClass()
#         cls.driver =  webdriver.Chrome()

#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.driver.quit()
#         super().tearDownClass()

#     def setUp(self) -> None:
#         self.user_password = "queenmary"
#         self.user =  User.objects.create_user('group37', 'some@gmail.com', self.user_password)
#         self.user.profile  =  Profile(city = "London", dob='2010-12-12')
#         self.user.profile.save()
#         self.user.save()
#         self.hobby  =  Hobby(name= "Basketball")



#         self.hobby.save()
#         self.hobby2  =  Hobby(name= "Football")



#         self.hobby2.save()
#         self.hobby.users.add(self.user)
#         self.hobby2.users.add(self.user)
#         return super().setUp()




#     def test_list_hobbies(self):

#         driver =  self.driver
#         url =  self.live_server_url + '/login/'
#         urlRedicrect=  self.live_server_url + reverse("mainapp:profile")
#         driver.get(url)

#         username_element  =  driver.find_element_by_id('id_username')
#         username_element.clear()
#         username_element.send_keys("group37")



#         password_element =  driver.find_element_by_id('id_password')
#         password_element.clear()
#         password_element.send_keys("queenmary")

#         driver.find_element_by_xpath("//input[@type='submit']").click()

#         time.sleep(5)

#         countHobbies   = len(driver.find_elements_by_xpath("//div[@id='hobbyContainer']/ul[@class='list-group']"))
#         areDisplaying = countHobbies  != 0



#         self.assertEqual(areDisplaying, True)