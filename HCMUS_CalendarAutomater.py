import crawlHTML
import postCalendar
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cookie', dest = 'cookie', default = 'none')
args = parser.parse_args()

def main():
    if(args.cookie == 'none'):
        crawlHTML.getScheduleJson()
    else:
        crawlHTML.getScheduleJsonWithCookie(Cookie = args.cookie)
    postCalendar.postCalendar(postCalendar.readJSON('TKB.json'))

if __name__ == '__main__':
    main()