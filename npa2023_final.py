#######################################################################################
# Yourname: Rata
# Your student ID: 655555
# Your GitHub Repo: 

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, and (restconf_final or netconf_final).

import json
import time
import requests
from restconf_final import create, delete, enable, disable, status

#######################################################################################
# 2. Assign the Webex hard-coded access token to the variable accessToken.

accessToken = "Bearer xxx"

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "yyy"
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": accessToken}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.find("/") == 0:  # ตรวจสอบว่าข้อความเริ่มต้นด้วย "/"
        try:
            # ดึงข้อความหลัง "/"
            space_index = message.find(" ")  # ค้นหาตำแหน่งของช่องว่างตัวแรก
            
            if space_index == -1:
                print("Error: No command provided")
                

            student_id = message[1:space_index]  # ดึง studentID โดยไม่รวม "/"
            command = message[space_index + 1:].strip()  # ดึงคำสั่งหลังจากช่องว่าง

            print(f"Student ID: {student_id}, Command: {command}")

            # 5. Complete the logic for each command
            if command == "create":
                responseMessage = create(student_id)
            elif command == "delete":
                responseMessage = delete(student_id)
            elif command == "enable":
                responseMessage = enable(student_id)
            elif command == "disable":
                responseMessage = disable(student_id)
            elif command == "status":
                responseMessage = status(student_id)
            else:
                responseMessage = responseMessage if 'responseMessage' in locals() else "No response generated."

            print(responseMessage)  # แสดงข้อความตอบกลับ

        except IndexError:
            print("Error: Invalid message format")
# 6. Complete the code to post the message to the Webex Teams room.
        
        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        postHTTPHeaders = HTTPHeaders = {"Authorization": accessToken, "Content-Type": "application/json"}

        # The Webex Teams POST JSON data
        # - "roomId" is is ID of the selected room
        # - "text": is the responseMessage assembled above
        postData = {"roomId": roomIdToGetMessages, "text": responseMessage}

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=json.dumps(postData),
            headers=postHTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
