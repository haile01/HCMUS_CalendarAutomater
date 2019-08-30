from bs4 import BeautifulSoup
import json
import re
def getLesson(cur : str):
    Lesson = re.search(r'\(.{0,}\)', cur, re.DOTALL)[0][1:-1]
    TimeStart = Lesson[ : Lesson.find('-')]
    TimeEnd = Lesson[Lesson.find('-') + 1 : ]
    Room = cur[cur.find('-', cur.find('-')+1) + 1 : ]

    Schedule = {
        "Thứ" : cur[1],
        "Tiết bắt đầu" : TimeStart,
        "Tiết kết thúc" : TimeEnd,
        "Cơ sở" : "Linh Trung - Thủ Đức" if (Room[Room.find(':') - 1] == '2') else "Nguyễn Văn Cừ - Quận 5",
        "Phòng" : Room[Room.find(':') + 1 : ]
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
        print("Progressing:", (id+1)/len(soup)*100, "%")
        for i in range(6):
            data[i] = re.search(r'>.{0,}<', str(data[i]), re.DOTALL)[0]
            data[i] = re.sub(r'\n|\t', '', data[i][1 : -1])
        
        curJson = {
            "Mã môn học" : data[0],
            "Tên môn học" : data[1],
            "Tên lớp" : data[2],
            "Loại" : "Thực hành" if data[3] == "TH" else "Lý thuyết",
            "Lịch học" : getLesson(data[4]),
            "Tuần bắt đầu" : data[5]
        }
        json_TKB[id] = curJson
        id+=1
    json.dump(json_TKB, WriteFile, indent=4)
