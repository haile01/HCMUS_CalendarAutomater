from bs4 import BeautifulSoup
import json
import re
def getLesson(cur : str):
    Lesson = re.search(r'\(.{0,}\)', cur, re.DOTALL)[0][1:-1]
    TimeStart = Lesson[ : Lesson.find('-')]
    TimeEnd = Lesson[Lesson.find('-') + 1 : ]
    Room = cur[cur.find('-', cur.find('-')+1) + 1 : ].strip()
    if (Room.find(':') == -1):
        CS = "Tại nhà"
        room = "Tại nhà"
    else:
        if (Room[Room.find(':') - 1] == '2'):
            CS = "Linh Trung - Thủ Đức"
        else:
            CS = "Nguyễn Văn Cừ - Quận 5"
        room = Room[Room.find(':') + 1 : ]
    Schedule = {
        "Day" : cur[1],
        "StartTime" : TimeStart,
        "EndTime" : TimeEnd,
        "Where" : CS,
        "Room" : room
    }
    return Schedule
def getScheduleJson(InputPath = 'TKB.html', OutputPath = 'TKB.json'):
    WriteFile = open(OutputPath, 'w')
    soup = BeautifulSoup(open(InputPath, 'rb').read(), 'html.parser')
    soup = soup.table.tbody.find_all('tr')
    json_TKB = {}
    id = 0
    for Subject in soup:
        data = Subject.find_all('td')
        #data[0] = ma mon
        #data[1] = ten mon
        #data[2] = ten lop
        #data[3] = loai
        #data[4] = lich hoc
        #data[5] = Tuan bat dau
        print(f"Progressing: {(id+1)/len(soup)*100 :.2f}%")
        for i in range(6):
            data[i] = re.search(r'>.{0,}<', str(data[i]), re.DOTALL)[0]
            data[i] = re.sub(r'\n|\t', '', data[i][1 : -1])
            data[i] = data[i].strip()
        day_pattern = r'\d\d/\d\d/\d\d\d\d'
        if re.search(day_pattern, data[5]) is None:
            continue
        curJson = {
            "SubjectID" : data[0],
            "SubjectName" : data[1],
            "ClassName" : data[2],
            "ClassType" : "Thực hành" if data[3] == "TH" else "Lý thuyết",
            "Schedule" : getLesson(data[4]),
            "StartWeek" : data[5]
        }
        json_TKB[id] = curJson
        id+=1
    json.dump(json_TKB, WriteFile, indent=4)
getScheduleJson()
