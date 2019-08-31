# HCMUS_CalendarAutomater
*A kindly simple way to have your HCMUS's timetable posted on Google Calendar*


**(Vietnamese in README-vi.md)**

## Installation

Clone this repository, then run this line on *command prompt/terminal* to install dependencies

>pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

After that, go to [this link](https://developers.google.com/calendar/quickstart/python) to download your `credentials.json` file to the current folder (and/or you can start reading tutorials from there and modify as you wish).

There are **two** ways for us to get your timetable template from the portal, that is crawling with your saved template, or giving us `Cookie` header after you have successfully logined

### If you want to go with your saved template

Access the [school's portal](http://portal.hcmus.edu.vn/), log in and go to `Đăng kí học phần > Kết quả ĐKHP`. Save the page's html with `Ctrl + s` as `TKB.html` in the cloned folder, which is `HCMUS_CalendarAutomater`.

Uptill now, files existing in current folder(`HCMUS_CalendarAutomater`) are:
* HCMUS_CalendarAutomater.py
* config.json
* crawlHTML.py
* postCalendar.py
* credentials.json
* TKB.html

Then run the code with command `python HCMUS_CalendarAutomater.py` 

### If you want to go with your cookie

After loging in your portal, turn on `Chrome's dev tool` by pressing `F12`, switch to `Network` tab, then refresh the page. Then, choose the first request whose name looks like `Default.apsx?pid=...`, search for `Cookie` in `Request Headers`, copy that whole line.

Now, go to your cloned folder, which is `HCMUS_CalendarAutomater`, run the following command

>python HCMUS_CalendarAutomater.py -c "your_copied_cookie"

## Config

If you want to update timetable of the current week, set `week` attribute as `this` inside `config.json` file, and if you want to update the upcoming week, set `week` as `that`

## Contribution

Thanks [Duy Thuc Le](https://github.com/leduykhongngu) for parsing from raw HTML to JSON database.

Thanks [Dinh Hai Le](https://github.com/pythagore1123) for uploading database with Calendar API.
