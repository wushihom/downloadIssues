from selenium import webdriver
import time

def main():
    b = webdriver.Chrome(executable_path="C:/dev/chromedriver/chromedriver.exe")
    b.get('https://www.baidu.com')
    time.sleep(5)
    b.quit()

if __name__ == '__main__':
    main()