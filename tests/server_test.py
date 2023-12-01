import unittest
from selenium import webdriver

class WebpageOpenTest(unittest.TestCase):
    def setUp(self):
        
        self.driver = webdriver.Chrome()

    def test_open_webpage(self):
        
        webpage_url = 'https://ultra-thought-397322.uc.r.appspot.com/'

        
        self.driver.get(webpage_url)

        
        expected_title = 'Text Summarizatio'
        actual_title = self.driver.title
        self.assertEqual(actual_title, expected_title, f"Expected title: {expected_title}, Actual title: {actual_title}")
        

    def tearDown(self):
        
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
