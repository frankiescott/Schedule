import requests
import configparser
import datetime
from bs4 import BeautifulSoup

def check_password_change(last_changed):
    #the portal page requires password changes every 30 days
    #the script will check when the last time the password
    date_to_check = datetime.datetime.strptime(last_changed, '%m-%d-%Y').date()
    today = datetime.date.today()
    if (today - date_to_check).days > 20:
        return True
    else:
        return False

def get_info():
    config = configparser.ConfigParser()
    config.read('C:\\Users\\Frankie\\Documents\\info.ini')
    credentials = dict()
    credentials.update({'userid': config['sr']['user']})
    credentials.update({'password': config['sr']['pass']})
    last_changed = config['sr']['passchange']

    if check_password_change(last_changed) is True:
        #creates new password by incrementing the last number
        num = int(credentials['password'][-1:])
        num = 1 if num is 9 else (num + 1)
        newpasswd = credentials['password'][:7] + str(num)

        #update password and last changed date in the file
        file = open('C:\\Users\\Frankie\\Documents\\info.ini', 'w')
        config.set('sr', 'pass', newpasswd)
        config.set('sr', 'passchange', datetime.date.today().strftime('%m-%d-%Y'))
        config.write(file)
        file.close()

        print("Password change needed.")
        #different parameters in the post request need to be supplied for a password change
        credentials.update({'newpassword1': newpasswd})
        credentials.update({'newpassword2': newpasswd})
    else:
        print("No password change needed.")

    return credentials

def login(credentials):
    session_requests = requests.session()
    login_url = 'https://member.wakefern.com/portalweb/servlet/com.wakefern.portal.servlets.ProcLogin'
    session_requests.post(login_url, data=credentials)
    page = session_requests.get('https://member.wakefern.com/portalweb/servlet/com.wakefern.portal.servlets.PortalHome?pageId=AEFC6E1A-A443-43FF-A7C8-5EF61147AA02')
    print_schedule(page)

def print_schedule(page):
    list = []
    soup = BeautifulSoup(page.text, 'html.parser')
    div = soup.find_all("div", id="p_p_content_")
    for tag in div:
        tdTags = tag.find_all("td", align="center")
        for tag in tdTags:
            list.append(tag.text)

    index = 0
    while index < len(list):
        i = 0
        while i < 6:
            print(list[i + index], end="\t")
            i = i + 1
        print("\n")
        index = index + 6

credentials = get_info()
login(credentials)
