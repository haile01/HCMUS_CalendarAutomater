import crawlHTML
import postCalendar
def main():
    crawlHTML.getScheduleJson(InputPath = 'TKB.html', OutputPath = 'TKB.json')
    postCalendar.postCalendar(postCalendar.readJSON('TKB.json'))
if __name__ == '__main__':
    main()