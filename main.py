import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading


BY_MAPPING = {
    "ID": By.ID,
    "NAME": By.NAME,
    "XPATH": By.XPATH,
    "CSS_SELECTOR": By.CSS_SELECTOR,
    "CLASS_NAME": By.CLASS_NAME,
    "TAG_NAME": By.TAG_NAME,
    "LINK_TEXT": By.LINK_TEXT,
    "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT
}

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def send_sms(config, phone):
    option = webdriver.EdgeOptions()
    option.add_argument('headless')
    browser = webdriver.Edge(options=option)
    browser.get(config["url"])
    time.sleep(config.get("initial_wait", 3))

    for action in config["actions"]:
        by = BY_MAPPING.get(action["by"])
        if not by:
            raise ValueError(f"Invalid locator type: {action['by']}")
        if action["type"] == "click":
            browser.find_element(by, action["value"]).click()
        elif action["type"] == "send_keys":
            browser.find_element(by, action["value"]).send_keys(phone)
        time.sleep(action.get("wait", 1))

    """
    TODO

    check 
    """
    browser.close()

def main():
    config_path = 'config.json'
    configs = load_config(config_path)

    phone = input('input：')

    """
    TODO
    error正确处理释放资源
    """
    while True:
        threads = []
        for name, config in configs.items():
            t = threading.Thread(target=send_sms, args=(config, phone))
            t.start()
            threads.append(t)

        # join
        for t in threads:
            t.join()

        print("fuking finished")

if __name__ == "__main__":
    main()
