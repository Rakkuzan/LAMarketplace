# LAMarketplace
LAMarketplace is a Lost Ark marketplace scrapper.

Since it got discovered here is a half-baked readme for those willing enough to make it work on their end.

## How does it work?
1. Take screenshot
2. Use text recognition.
3. Save data to Google Sheets


## Installation
1. Install tesseract and move it to ./bin  
https://github.com/UB-Mannheim/tesseract/wiki
2. Create new Google Sheets
3. In created sheets add new tab called "**RAW DATA**"
4. Create new project in https://console.cloud.google.com/
5. Add Google Sheets API into it.
6. Create new service account
7. Create new private key for this account.
8. Rename the file you just downloaded to credentials.json and move it to ./
9. Share your sheets with the account you created.
10. Get the ID of your sheets from the link.
11. in ./ create file called ids.json
```json
{
    "sheet_id": "YOUR_SHEET_ID_HERE"
}
```
12. In Lost Ark move your marketplace windows to upper left corner.
13. Choose the tab you want to scan.
14. Optionally move your character somewhere dark to improve text recognition.
15. Run the bot.