# HCMUS_CalendarAutomater
*A kindly simple way to have your HCMUS's timetable posted on Google Calendar*

## Installation

Clone this repository, then run this line on *command prompt/terminal* to install dependencies

>pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

After that, go to [this link](https://developers.google.com/calendar/quickstart/python) to download your `credentials.json` file to the current folder (and/or you can start reading tutorials from there and modify as you wish).

Then, access the [school's portal](http://portal.hcmus.edu.vn/), log in and go to `Đăng kí học phần > Kết quả ĐKHP`. Save the page's html with `Ctrl + s` and save as `TKB.html` in `HCMUS_CalendarAutomater` folder.

Uptill now, files existing in current folder are:
* HCMUS_CalendarAutomater.py
* config.json
* crawlHTML.py
* postCalendar.py
* credentials.json
* TKB.html

Then run the code with command `python HCMUS_CalendarAutomater.py` 

## Config

If you want to update time table of the current week, set `week` attribute as `this` inside `config.json` file, and if you want to update the upcoming week, set `week` as `that`

## Contribution

Thanks [Duy Thuc Le](https://github.com/leduykhongngu) for parsing from raw HTML to JSON database.

Thanks [Dinh Hai Le](https://github.com/pythagore1123) for uploading database with Calendar API.
