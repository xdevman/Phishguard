import subprocess
import os
from pymongo import MongoClient
from datetime import datetime, timezone
import gridfs

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_phishing']
collection = db['phishing_tweets']
fs = gridfs.GridFS(db)

# Ensure the collection has a unique index on tweet_id to optimize performance
collection.create_index("tweet_id", unique=True)

# Directory for temporary screenshots
SCREENSHOT_DIR = '/root/PishGuard/Screenshot_tmp/'

def take_screenshot(tweet_link, tweet_id):

    # Run the tweetcapture command in the screenshot directory
    os.chdir(SCREENSHOT_DIR)
    # Construct the full file path for the screenshot
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{tweet_id}.png")
    
    # Run the tweetcapture command with the specified output directory and filename
    result = subprocess.run(['tweetcapture', tweet_link, '-o', screenshot_path], capture_output=True, text=True)
    
    os.chdir('..')  # Return to the original directory
    
    # Check if the screenshot was successfully saved
    if os.path.exists(os.path.join(SCREENSHOT_DIR, f"{tweet_id}_tweetcapture.png")):
        return True
    else:
        print(f"Failed to capture screenshot for {tweet_link}: {result.stderr}")
        return False

def save_screenshot_to_gridfs(tweet_id):
    # Read the screenshot file
    file_path = os.path.join(SCREENSHOT_DIR, f"{tweet_id}.png")
    with open(file_path, 'rb') as f:
        screenshot = f.read()
    
    # Save the screenshot to GridFS
    file_id = fs.put(screenshot, filename=f"{tweet_id}.png", encoding='utf-8')
    
    # Delete the local screenshot file
    os.remove(file_path)
    
    return file_id
    
# Function to insert or update a tweet report
def report_tweet(tweet_id, text, link, username, created_time, tweet_link):
    screenshot_id = take_screenshot(tweet_link, tweet_id)
    save_screenshot_to_gridfs(tweet_id)
    # Attempt to update the document
    result = collection.update_one(
        {"tweet_id": tweet_id},
        {
            "$set": {
                "text": text,
                "link": link,
                "username": username,
                "created_time": created_time,
                "screenshot_id": screenshot_id,
                "tweet_link": tweet_link,
                "last_reported_time": datetime.utcnow(),
                "status": "not_checked"
            },
            "$inc": {"report_count": 1}
        }
    )
    
    # If the document did not exist and was not updated, insert it
    if result.matched_count == 0:
        collection.insert_one(
            {
                "tweet_id": tweet_id,
                "text": text,
                "link": link,
                "username": username,
                "created_time": created_time,
                "screenshot_id": screenshot_id,
                "tweet_link": tweet_link,
                "last_reported_time": datetime.utcnow(),
                "status": "not_checked",
                "report_count": 1,
                "reported_to_sites": []
            }
        )

# Function to set tweet status to 'processing'
def set_processing(tweet_id):
    collection.update_one(
        {"tweet_id": tweet_id},
        {"$set": {"status": "processing"}}
    )

# Function to validate a tweet and set status to 'valid'
def validate_tweet(tweet_id):
    collection.update_one(
        {"tweet_id": tweet_id},
        {"$set": {"status": "valid"}}
    )

# Function to report the tweet to a phishing detection site
def report_to_site(tweet_id, site_name):
    collection.update_one(
        {"tweet_id": tweet_id},
        {"$addToSet": {"reported_to_sites": site_name}}  # Add the site to reported_to_sites array if not already present
    )

# Example usage to report a tweet
report_tweet(
    tweet_id="1785367640950599974",
    text="Check out this link for a free giveaway! http://phishing-link.com",
    link="http://phishing-link.com",
    username="phisher123",
    created_time=datetime(2024, 5, 25, 12, 34, 56),
    tweet_link="https://x.com/xdevman/status/1785367640950599974"
)

# Example usage to set tweet status to 'processing'
set_processing("1785367640950599974")

# Example usage to validate a tweet
validate_tweet("1785367640950599974")

# Example usage to report the tweet to a phishing detection site
report_to_site("1785367640950599974", "Metamask")
