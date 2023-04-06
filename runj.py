import os
import sys
import time
from collections import Counter
import cv2
import urllib
from smtplib import SMTP
from numpy import array
import urllib.request as ur
from time import sleep
import pickle
import face_recognition as fr
threshold_value = 0
ip_address = 0


try:
    os.chdir("DATASETS")
except:
    pass


def train():
    def Train_user_images():
        try:
            USER_NAMES = open("user_naming_order.dll", 'a+')
        except:
            pass
        else:
            USER_NAMES.close()
        data = os.listdir()
        x = [_ for _ in data if _.endswith('g')]
        USER_NAMES_INITIAL = open(
            "user_naming_order.dll", 'r').read().split("\n")
        try:
            known_mail_names = open("mail_info.dll", 'a+')
        except:
            pass
        else:
            known_mail_names.close()
        for _ in x:
            hold_name = _.split('.')[0]
            image = _
            USER_NAMES = open("user_naming_order.dll", 'a+')
            USER_NAMES.close()
            known_mail_names = open("mail_info.dll", "a+").read().split("\n")
            if hold_name not in (set(USER_NAMES_INITIAL) or set(known_mail_names)):
                mail_file = open("mail_info.dll", "a+")
                mail_file.write(hold_name+"\n")
                mail_file.close()
            user_image = fr.load_image_file(image)
            user_image_encoding = fr.face_encodings(user_image)
            DATA_SET_FILE = open("images_encoding.dll", 'a+')
            DATA_SET_FILE.write(
                str(list(user_image_encoding[0]))+'----------\n')
            DATA_SET_FILE.close()
            USER_NAMES = open("user_naming_order.dll", "a+")
            USER_NAMES.write(image.split('.')[0]+'\n')
            USER_NAMES.close()
            print("Training ....")
        sleep(1)
        for _ in x:
            os.remove(_)
    try:
        os.chdir("DATASETS")
    except:
        pass
    test = open("root.dll", "r")
    test.close()
    Train_user_images()
    registered_mails = open("registered_mails.dll", "a+")
    registered_mails.close()
    mails_to_ask = open("mail_info.dll", "r").read().split("\n")
    mails_to_ask.remove(mails_to_ask[-1])

    def get_mail_id(user_name):
        user_input = mail_id
        registered_mails = open("registered_mails.dll", "a+")
        registered_mails.write(user_name+","+user_input+"\n")
        registered_mails.close()
    registered_users = open("registered_mails.dll", "r").read().split("\n")
    registered_user_names = [_.split(",")[0] for _ in registered_users]
    mails_to_ask = set(mails_to_ask)
    for _ in mails_to_ask:
        if _ not in registered_user_names:
            print("Enter Email ID : ")
            mail_id = input()
            get_mail_id(_)


def detect():
    def send_mail_to_users():
        data = pickle.load(open("present.dll", "rb"))
        count = Counter(data)
        file = open("root.dll", "r").read().split("|")
        mail = SMTP("smtp.gmail.com", 587)
        mail.ehlo()
        mail.starttls()
        mail.login(file[0], file[1])
        DICTIONARY = {}
        mail_file = open("registered_mails.dll").read().split("\n")
        for _ in mail_file:
            try:
                user_name = _.split(",")[0]
                user_mail = _.split(",")[1]
                DICTIONARY[user_name] = user_mail
            except:
                pass
        absent_count = 0
        try:
            threshold = int(threshold_value)
        except:
            print("Invalid Values !!")

        else:
            for _ in count.keys():
                try:
                    if count[_] < threshold:
                        absent_count += 1
                        mail.sendmail(
                            "alert.com", DICTIONARY[_], "Please be regular "+_)
                except:
                    pass

            print("Total students declared absent : "+str(absent_count))
            print("Mail sent to all the irregular students")
            mail.close()

    def return_encodings(problem):
        x = problem.split('\n')
        p = "".join(x)
        known_face_encodings.append(list(map(float, p.split(','))))
    ENCODINGS = "images_encoding.dll"
    USER_NAMES = "user_naming_order.dll"
    try:
        users = open(USER_NAMES).read().split('\n')
    except:
        pass
    else:
        known_face_names = users[0:len(users)-1]
        known_face_encodings = []
        encoding = open(ENCODINGS).read().split('----------')
        for _ in range(len(users)-1):
            encoding[_] = encoding[_].replace("[", "")
            encoding[_] = encoding[_].replace("]", "")
            return_encodings(encoding[_])

        def present_details():
            try:
                os.remove("present.dll")
            except:
                pass
            finally:
                my_file = open("present.dll", "wb")
                pickle.dump(present_count_db, my_file)
                my_file.close()
                send_mail_to_users()
        url = "http://"+ip_address+"/shot.jpg"
        known_face_names = known_face_names
        known_face_encoding = known_face_encodings
        face_locations = []
        face_encodings = []
        face_names = []
        present_count_db = []
        present_count_db.extend(set(known_face_names))
        process_this_frame = True
        try:
            while True:
                s = urllib.request.urlopen(url)
                imgnp = array(bytearray(s.read()))
                frame = cv2.imdecode(imgnp, -1)
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                if process_this_frame:
                    face_locations = fr.face_locations(rgb_small_frame)
                    face_encodings = fr.face_encodings(
                        rgb_small_frame, face_locations)
                    face_names = []
                    for face_encoding in face_encodings:
                        matches = fr.compare_faces(
                            known_face_encoding, face_encoding, tolerance=0.5)
                        name = "UNKNOWN"
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                            present_count_db.append(name)
                        face_names.append(name)
                process_this_frame = not process_this_frame
                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom),
                                  (255, 204, 102), 5, cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left+6, bottom-6),
                                font, 1.0, (26, 255, 26), 2)
                cv2.imshow("VIDEO", frame)
                if cv2.waitKey(1) & 0xff == ord('q'):
                    break
            cv2.destroyAllWindows()
            present_details()
            time.sleep(5)
        except:
            print("Network error")
            print("Please check your connection")
            print("Make sure your PHONE & DEVICE are connected via same network")


print("Welcome to Smart_Attendence!")
print("Please select an option : ")
print("Type 1: Perform training")
print("Type 2: Take Attendence")
x = input()
if x == '1':
    train()
else:
    print("Enter the ip of your cam : ")
    ip_address = input()
    print("Enter a threshold for absent days : ")
    threshold_value = input()
    detect()