import json, requests
import time, os, sys
import random, platform
import threading, hashlib

global response, delay

token = ""
Origin = "https://prod-app7790408-eb1dff25c660.pages-ac.vk-apps.com"
Referer = "https://prod-app7790408-eb1dff25c660.pages-ac.vk-apps.com/"
UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 OPR/75.0.3969.149"

headers = {
    "Content-Type": "application/json",
    "authorization": "Bearer " + token,
    "origin": Origin,
    "referer": Referer,
    "user-agent": UserAgent,
}

GameConfig = {
    "Balance" : {
        "Coins" : 0,
        "Money" : 0,
        "Fetters" : 0,
        "GoldFetters" : 0
    },
    "AccountInfo": {
        "UID" : None,
        "CurrentIncome" : None,
        "Job" : None,
        "Referal" : None,
        "Profit" : None,
        "Slaves" : None,
        "MaxSlaves" : None,
        "Room" : None,
        "FettersTime" : None
    },
    "Errors" : None,
    "Task": {
        "Task" : None,
        "Number" : None
    }
}

AccountJSON = None
Work = True
delay = float(random.uniform(3.40, 4.0))

#Settings
UpgradeLimited = 1.0, 11.0 # Диапазон прибыли рабов в котором будет работать автоматическое улучшение
MaxProfit = 10.0 # Максимальный доход раба, при котором ещё возможна его покупка

CheckInApp = True # Выполнение проверки входа пользователя в приложение
Act_GetBonus = True # Функция автоматической сборки бонусов
Act_UpgradeSlaves = True # Функция автоматеческого улучшения рабов
Act_DeleteNoWalidSlaves = True # Функция удаления невыгодных для улучшения рабов
Act_FetterSlaves = True # Функция автоматической установки оков рабам
Act_BuyTop = True # Функция выкупа рабов у Топа по монетам
Act_RestoringSlaves = False # Функция восстановления потеряных рабов
SkipDisabledTasks = True # Функция пропуска пакетов не выбраных в настройках

def ConfigurationScreen():
    while True:
        try:
            _dir_ = Path + 'Data/SlavesID/'
            Config = "\033[33m {}".format("\r     ●▬▬▬▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬▬▬▬●\n")
            Config = Config + "\033[31m {}".format("░░░░░░░░░ Bot 2.2 by Seffel2274 ░░░░░░░░░\n")
            Config = Config + "\033[33m {}".format("    ●▬▬▬▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬▬▬▬●\n\n")
            Config = Config + "\nBalance >> Coins:             " + str(GameConfig["Balance"]["Coins"])
            Config = Config + "\n           Money:             " + str(GameConfig["Balance"]["Money"])
            Config = Config + "\n           Fetters:           " + str(GameConfig["Balance"]["Fetters"])
            Config = Config + "\n           Gold Fetters:      " + str(GameConfig["Balance"]["GoldFetters"]) + "\n"
            Config = Config + "\nActions >> Task:              " + str(GameConfig["Task"]["Task"])
            Config = Config + "\n           Number of tasks:   " + str(GameConfig["Task"]["Number"])
            Config = Config + "\n           Number stored IDs: " + str(len(os.listdir(_dir_))) + "\n"
            Config = Config + "\nAccount >> ID:                " + str(GameConfig['AccountInfo']['UID'])
            Config = Config + "\n           Profit:            " + str(GameConfig['AccountInfo']['CurrentIncome'])
            Config = Config + "\n           Number of slaves:  " + str(GameConfig['AccountInfo']['Slaves']) + " / " + str(GameConfig['AccountInfo']['MaxSlaves'])
            Config = Config + "\n           Profit Referal:    " + str(GameConfig['AccountInfo']['Profit']) 
            Config = Config + "\n           Job:               " + str(GameConfig['AccountInfo']['Job']) 
            Config = Config + "\n           Referal:           " + str(GameConfig['AccountInfo']['Referal'])  + "\n"
            Config = Config + "\nError >>   " + str(GameConfig['Errors'])
            GameConfig['Errors'] = None
            print(Config)
        except Exception as error:
            GameConfig['Errors'] = str('ConfigurationScreen >> ' + str(error))
        time.sleep(0.5); NoLog()

def NoLog():

    if platform.system() == "Windows":
        os.system('color 6')
        os.system("cls")
    elif platform.system() == "Linux":
        os.system('PS1="\\[\\e[1;91m\\]\\u@\\h\\[\\e[m\\]:\\[\\e[1;96m\\]\\w\\[\\e[1;92m\\]\\\\$ "')
        os.system("clear")
    else:
        print("No command to system: " + platform.system())

def Account():
        global AccountJSON
        while True:
                try:
                    def MathMaxSlaves(Rang):

                                if Rang == 0:
                                        return 50

                                elif Rang == 1:
                                        return 100

                                elif Rang == 2:
                                        return 500

                                elif Rang == 3:
                                        return 1000

                                elif Rang == 4:
                                        return 2500

                                elif Rang == 5:
                                        return 5000

                                elif Rang == 6:
                                        return 10000

                                else:
                                        return 50000

                    AccountJSON = requests.get(f"https://slave.su/api/user/me",
                                headers=headers).json()
                    GameConfig['AccountInfo']['UID'] = int(AccountJSON['user']['vk_user_id'])
                    GameConfig['AccountInfo']['Slaves'] = int(AccountJSON['user']['slaves_count'])
                    GameConfig['AccountInfo']['Referal'] = AccountJSON['user']['ref']
                    GameConfig['AccountInfo']['CurrentIncome'] = float(AccountJSON['user']['slaves_profit_per_min'])
                    GameConfig['AccountInfo']['Job'] = str(AccountJSON['user']['job'])
                    GameConfig['AccountInfo']['Room'] =int( AccountJSON['user']['room'])
                    GameConfig['AccountInfo']['Profit'] = float(AccountJSON['user']['profit_per_min'])
                    GameConfig['AccountInfo']['MaxSlaves'] = int( MathMaxSlaves(int(AccountJSON['user']['room'])))
                    GameConfig['AccountInfo']['FettersTime'] = int(AccountJSON['user']['fetter_minutes'])
                    GameConfig["Balance"]["Coins"] = int(AccountJSON['user']['balance']['coins'])
                    GameConfig["Balance"]["Money"] = int(AccountJSON['user']['balance']['money'])
                    GameConfig["Balance"]["Fetters"] = int(AccountJSON['user']['balance']['fetters'])
                    GameConfig["Balance"]["GoldFetters"] = int(AccountJSON['user']['balance']['gold_fetters'])
                    with open(Path + "Data/Settings/Settings.json", "w") as GameConfig_JSON:
                        json.dump(GameConfig, GameConfig_JSON, indent=4)
                    if "slaves" in AccountJSON.keys():
                        for Slaves in AccountJSON['slaves']:
                            if os.path.exists(Path + "Data/SlavesID/" + str(Slaves["vk_user_id"]) + ".json") == False:
                                with open(Path + "Data/SlavesID/" + str(Slaves["vk_user_id"]) + ".json", "w") as UsersJSON:
                                    json.dump(Slaves, UsersJSON, indent=4)
                    time.sleep(float(random.uniform(1.5, 3.0)))
                except Exception as error:
                        GameConfig['Errors'] = str('Account >> ' + str(error))
                        with open(Path + "Data/Settings/Settings.json", "w") as GameConfig_JSON:
                            json.dump(GameConfig, GameConfig_JSON, indent=4)

def Methods(Method, id = None):

    try:

        if Method == "get_bonus":

            if Act_GetBonus == True:
                return str(requests.post("https://slave.su/api/bonuses/earn",
                        headers=headers, json={"type": "bonus:rewarded_ad"}))
            else:
                if SkipDisabledTasks == True:
                    return "NoDelay"
                else:
                    return str(requests.post("https://slave.su/api/bonuses/earn",
                            headers=headers, json={"type": "bonus:rewarded_ad"}))

        if Method == "buy_slaves":

            if Act_BuyTop == True:
                return requests.post("https://slave.su/api/slaves/buySlave",
                        headers=headers, json={"slave_id": id}).json()
            else:
                if SkipDisabledTasks == True:
                    return "NoDelay"
                else:
                    return requests.post("https://slave.su/api/slaves/buySlave",
                            headers=headers, json={"slave_id": id}).json()

        if Method == "get_userinfo":
            return requests.get(f"https://slave.su/api/slaves/user/{id}",
                    headers=headers).json()

        if Method == "get_slaveslist":

            return requests.get(f"https://slave.su/api/slaves/slaveList/{id}",
                    headers=headers).json()

        if Method == "get_topmoneyuser":
            return requests.get("https://slave.su/api/slaves/topUsers",
                    headers=headers).json()

        if Method == "set_fetters":

            if Act_FetterSlaves == True:
                return requests.post("https://slave.su/api/slaves/setFetters",
                        headers=headers, json={"slave_id": id}).json()
            else:
                if SkipDisabledTasks == True:
                    return "NoDelay"
                else:
                    return requests.post("https://slave.su/api/slaves/setFetters",
                            headers=headers, json={"slave_id": id}).json()
    
        if Method == "set_upgrade":

            if Act_UpgradeSlaves == True:
                return requests.post("https://slave.su/api/slaves/upgradeSlave",
                        headers=headers, json={"slave_id": id}).json()
            else:
                if SkipDisabledTasks == True:
                    return "NoDelay"
                else:
                    return requests.post("https://slave.su/api/slaves/upgradeSlave",
                            headers=headers, json={"slave_id": id}).json()

        if Method == "set_delete":

            if Act_DeleteNoWalidSlaves == True:
                return requests.post("https://slave.su/api/slaves/saleSlave",
                        headers=headers, json={"slave_id": id}).json()
            else:
                if SkipDisabledTasks == True:
                    return "NoDelay"
                else:
                    return requests.post("https://slave.su/api/slaves/saleSlave",
                            headers=headers, json={"slave_id": id}).json()

        if Method == "get_toprefuser":
            return requests.post("https://slave.su/api/slaves/topUsersRefs",
                    headers=headers, json={"slave_id": id}).json()
            
    except Exception as error:
        GameConfig['Errors'] = str('Methods >> ' + str(error))

def TaskManager():

    try:
        global response, delay
        delay = float(random.uniform(3.40, 4.0))
        _dir_ = Path + 'Data/Task/'
        while True:
            TaskList = os.listdir(_dir_)
            GameConfig["Task"]["Number"] = len(TaskList)
            if len(TaskList) >= 0:
                for Task in TaskList:
                    try:
                        with open(_dir_ + Task, "r") as read_file:
                            TaskData = json.load(read_file)
                        if TaskData['Performance'] == False:
                            if TaskData['Money'] == 0 or int(GameConfig["Balance"]["Coins"]) > int(TaskData['Money']):
                                GameConfig["Task"]["Task"] = TaskData["Task"]
                                response = Methods(TaskData["Task"], TaskData["id"])
                                if not response == "NoDelay":
                                        time.sleep(delay)
                                        delay = float(random.uniform(3.40, 4.0))
                                        if not "error" in response:
                                            TaskData["Performance"] = True
                                            with open(_dir_ + Task, "w") as write_file:
                                                json.dump(TaskData, write_file, indent=4)
                                            os.remove(_dir_ + Task)
                        else:
                            os.remove(_dir_ + Task)
                    except Exception as error:
                            os.remove(_dir_ + Task)
                            GameConfig['Errors'] = str('TaskManager >> ' + str(error))
            time.sleep(0.5)
            
    except Exception as error:
        GameConfig['Errors'] = str('TaskManager >> ' + str(error))

def TaskSchedulerWrite(Task, Data = None, Money = 0):
    try:

        if Task == "buy_slaves":
                Blank = {
                        'Task' : "buy_slaves",
                        'id' : Data,
                        "Performance" : False,
                        "Money" : Money
                }
        if Task == "set_delete":
                Blank = {
                        'Task' : "set_delete",
                        'id' : Data,
                        "Performance" : False,
                        "Money" : Money
                }
        if Task == "set_upgrade":
                Blank = {
                        'Task' : "set_upgrade",
                        'id' : Data,
                        "Performance" : False,
                        "Money" : Money
                }
        if Task == "set_fetters":
                Blank = {
                        'Task' : "set_fetters",
                        'id' : Data,
                        "Performance" : False,
                        "Money" : Money
                }
        if Task == "get_bonus":
                Blank = {
                        'Task' : "get_bonus",
                        'id' : None,
                        "Performance" : False,
                        "Money" : Money
                }
        Name = hashlib.sha256(str(Blank).encode()).hexdigest()
        if os.path.exists(Path + "Data/Task/" + Name + ".json") == False:
            with open(Path + "Data/Task/" + Name + ".json", "w") as Blank_JSON:
                    json.dump(Blank, Blank_JSON, indent=4)
                    

    except Exception as error:
        GameConfig['Errors'] = str('TaskSchedulerWrite >> ' + str(error))

def GetBonus():

    while True:
        TaskSchedulerWrite(Task = "get_bonus")
        time.sleep(60.0);

def DeleteNoWalidSlaves():

    while True:
        try:
            if "slaves" in AccountJSON.keys():
                for Slaves in AccountJSON['slaves']:
                    if float(str(float(Slaves['profit_per_min'])%1)[:4]) > 0.02:
                       TaskSchedulerWrite("set_delete", int(Slaves['vk_user_id']));

                       time.sleep(0.1)
            time.sleep(5)
        except Exception as error:
            GameConfig['Errors'] = str('DeleteNoWalidSlaves >> ' + str(error))
        time.sleep(1.5)

def UpgradeSlaves():

    while True:
        try:
            if "slaves" in AccountJSON.keys():
                for Slaves in AccountJSON['slaves']:
                    if float(Slaves["profit_per_min"]) >= float(UpgradeLimited[0]) and float(Slaves["profit_per_min"]) <= float(UpgradeLimited[1]):
                        if not float(str(float(Slaves['profit_per_min'])%1)[:4]) > 0.02:
                            TaskSchedulerWrite("set_upgrade", int(Slaves['vk_user_id']), int(Slaves['price']))
            time.sleep(5)
        except Exception as error:
            GameConfig['Errors'] = str('UpgradeSlaves >> ' + str(error))
        time.sleep(1)

def FetterSlaves():

    while True:
        try:
            if "slaves" in AccountJSON.keys():
                for Slaves in AccountJSON['slaves']:
                    if int(Slaves["fetter_to"]) == 0:
                        TaskSchedulerWrite("set_fetters", int(Slaves['vk_user_id']))
            time.sleep(5)
        except Exception as error:
            GameConfig['Errors'] = str('FetterSlaves >> ' + str(error))
        time.sleep(1)

def BuyTop():
    while True:
        try:
            Users = Methods("get_topmoneyuser")
            if "list" in Users.keys():
                for User in Users["list"]:
                    TopSlaves = Methods("get_userinfo", User["vk_user_id"])
                    if not float(str(float(TopSlaves['profit_per_min'])%1)[:4]) > 0.02:
                        if MaxProfit > float(TopSlaves['profit_per_min']):
                            if TopSlaves["fetter_to"] == 0:
                                TaskSchedulerWrite("buy_slaves", TopSlaves["vk_user_id"], int(TopSlaves["price"]))

                    SlavesInf = Methods("get_slaveslist", User["vk_user_id"])
                    if "list" in SlavesInf.keys():
                        for Slaves in SlavesInf["list"]:
                            if not float(str(float(Slaves['profit_per_min'])%1)[:4]) > 0.02:
                                if MaxProfit > float(Slaves['profit_per_min']):
                                    if Slaves["fetter_to"] == 0:
                                        if CheckInApp == False:
                                            was_in_app = True
                                        else:
                                            was_in_app = Slaves["was_in_app"]

                                        if was_in_app == True:
                                                TaskSchedulerWrite("buy_slaves", Slaves["vk_user_id"], int(Slaves["price"]))
                    else:
                        time.sleep(delay)
            else:
                time.sleep(delay)
        except Exception as error:
            GameConfig['Errors'] = str('BuyTop >> ' + str(error))

def RestoringSlaves():
    try:
        delay = float(random.uniform(3.40, 4.0))
        _dir_ = Path + 'Data/SlavesID/'
        SlavesID = os.listdir(_dir_)
        if len(SlavesID) >= 0:
            for SlavesJSON in SlavesID:
                with open(_dir_ + SlavesJSON, "r") as read_file:
                    SlavesData = json.load(read_file)
                Data = Methods("get_userinfo", SlavesData["vk_user_id"])
                if not str(Data["ref"]) == str(GameConfig['AccountInfo']['UID']):
                    if Data["fetter_to"] == 0:
                        TaskSchedulerWrite("buy_slaves", Data["vk_user_id"], int(Data["price"]))
                time.sleep(float(random.uniform(3.5, 4.0)))
    except Exception as error:
            GameConfig['Errors'] = str('RestoringSlaves >> ' + str(error))

if __name__ == "__main__":

    Path = str(os.path.abspath(os.curdir)).replace("\\", "/") + "/"

    Dirs = ['Data/Task', 'Data/Settings', 'Data/SlavesID']
    
    for Dir in Dirs:

        Dir = Path + Dir
        if not os.path.exists(Dir):
            os.makedirs(Dir)

    threading.Thread(target=ConfigurationScreen).start()
    threading.Thread(target=Account).start()

    while True:
                if not AccountJSON == None:

                    threading.Thread(target=TaskManager).start()
                    
                    if Act_RestoringSlaves == True:
                            threading.Thread(target=RestoringSlaves).start()
                    if Act_GetBonus == True:
                            threading.Thread(target=GetBonus).start()
                    if Act_UpgradeSlaves == True:
                            threading.Thread(target=UpgradeSlaves).start()
                    if Act_DeleteNoWalidSlaves == True:
                            threading.Thread(target=DeleteNoWalidSlaves).start()
                    if Act_FetterSlaves == True:
                            threading.Thread(target=FetterSlaves).start()
                    if Act_BuyTop == True:
                            threading.Thread(target=BuyTop).start()
                    break
                time.sleep(1)

    while Work:
        time.sleep(1)
