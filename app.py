from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

app = Flask(__name__)

# Configure Chrome WebDriver
def get_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless if you don't need a browser window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Static website URL and root div ID
STATIC_URL = "https://transaction-appv1.netlify.app"
ROOT_DIV_ID = "root"  # Replace with your actual root div ID

def keep_website_alive():
    driver = get_webdriver()
    try:
        while True:
            try:
                # Navigate to the static website URL
                driver.get(STATIC_URL)

                # Find the root div element by its ID
                element = driver.find_element(By.ID, ROOT_DIV_ID)

                # Perform a click action to keep the website active
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()

                print(f"Successfully clicked on the root div with ID {ROOT_DIV_ID}")
            except Exception as e:
                print(f"Error occurred: {str(e)}")

            # Wait before the next iteration to avoid excessive requests
            time.sleep(60)  # Adjust the interval as needed
    finally:
        driver.quit()

# Route to start keeping the website alive
@app.route('/start_keep_alive', methods=['GET'])
def start_keep_alive():
    try:
        # Start the background thread to keep the website alive
        thread = threading.Thread(target=keep_website_alive, daemon=True)
        thread.start()
        return jsonify({"status": "Success", "message": "Keep-alive process started."}), 200
    except Exception as e:
        return jsonify({"status": "Error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
