# PhishGuard: Twitter Phishing Detection Bot

PhishGuard is a Twitter bot designed to detect and report phishing tweets on the platform. Users can tag the bot in suspicious tweets, which are then collected, analyzed, and reported to phishing detection services like Metamask.

## How to Use PhishGuard

### 1. Tagging the Bot

To report a phishing tweet, simply tag the PhishGuard bot in the suspicious tweet on Twitter. You can do this by mentioning the bot's username in a reply to the tweet or by directly tagging the bot in the tweet itself.

### 2. Phishing Tweet Detection

Once tagged, PhishGuard will automatically collect the following information from the reported tweet:

- Text of the tweet
- Phishing link (if present)
- Username of the tweet author
- Tweet link
- Timestamp of tweet creation

Additionally, PhishGuard will take a screenshot of the reported tweet for further analysis.

### 3. Database Storage

The collected information is then saved into a MongoDB database for further processing and analysis. PhishGuard checks for duplicate reports to avoid spamming phishing detection services.

### 4. Reporting to Phishing Detection Services

PhishGuard validates the reported tweets to ensure accuracy. Validated reports are then automatically reported to phishing detection services like Metamask for further action.

### 5. Monitoring and Analysis

PhishGuard provides a single-page interface to monitor and analyze detected phishing links, fake user accounts, and reports sent to phishing detection services.

## Contributing

Contributions to PhishGuard are welcome! If you have suggestions for improvements, feature requests, or bug reports, please open an issue or submit a pull request.

## Contact

For questions or inquiries about PhishGuard, contact the project team:
- Email: xd3vman@gmail.com
- 
## Tasks

- [ ] Screenshot feature
- [ ] Tweet reader with API
- [ ] Main file and handle files

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
