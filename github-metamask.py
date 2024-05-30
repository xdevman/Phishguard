from pymongo import MongoClient
from github import Github

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_phishing']
collection = db['phishing_tweets']

# Authentication using Personal Access Token
token = 'your_personal_access_token'
github = Github(token)

# Replace 'owner' and 'repository' with the actual owner and repository name
repo = github.get_repo('MetaMask/eth-phishing-detect')

def check_validity_and_report(tweet_id):
    # Retrieve the tweet document from MongoDB
    tweet = collection.find_one({"tweet_id": tweet_id})
    if not tweet:
        print(f"Tweet with ID {tweet_id} not found in the database.")
        return
    
    # Check if the tweet is already validated
    if tweet.get("status") == "valid":
        print(f"Tweet with ID {tweet_id} is already validated.")
        return
    
    # Perform validation checks (replace this with your validation logic)
    is_valid = True  # Placeholder for validation logic

    if is_valid:
        # Extract phishing domain from the tweet document
        phishing_domain = tweet.get("link", "")
        
        # Check if phishing domain is empty
        if phishing_domain:
            # Extract screenshot link from the tweet document
            screenshot_link = tweet.get("screenshot_url", "")
            
            # Define issue title template
            issue_title_template = "[Block Phishing Domain]"

            # Define issue body template with placeholders for phishing domain and screenshot link
            issue_body_template = f"""
            **Phishing Domain:** {phishing_domain}
            """
            if screenshot_link:
                issue_body_template += f"\n**Tweet Screenshot:** {screenshot_link}\n"

            issue_body_template += """
            This issue is being created to report a phishing domain.

            Please investigate and take appropriate action.

            - [ ] I have checked to make sure that there is not a duplicate issue.
            """

            # Construct the issue title
            issue_title = f"{issue_title_template} - {phishing_domain}"

            # Construct the issue body
            issue_body = issue_body_template

            # Create the new issue
            new_issue = repo.create_issue(title=issue_title, body=issue_body)

            print(f"New issue created: {new_issue.html_url}")
            
            # Update the MongoDB document to mark the tweet as valid
            collection.update_one({"tweet_id": tweet_id}, {"$set": {"status": "valid"}})
            
            # Check if the tweet has been reported to Metamask before
            if "Metamask" not in tweet.get("reported_to_sites", []):
                # Update the reported_to_sites field in MongoDB to indicate that the tweet has been reported to Metamask
                collection.update_one({"tweet_id": tweet_id}, {"$addToSet": {"reported_to_sites": "Metamask"}})
                print(f"Tweet with ID {tweet_id} reported to Metamask.")
            else:
                print(f"Tweet with ID {tweet_id} already reported to Metamask.")
        else:
            print(f"Skipping tweet with ID {tweet_id} because phishing domain is empty.")
    else:
        print(f"Tweet with ID {tweet_id} is not a valid phishing tweet.")

# Example usage:
check_validity_and_report("1234567890")
