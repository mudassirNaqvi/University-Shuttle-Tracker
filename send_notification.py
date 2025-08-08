import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("D:/Gps/service-account.json")
firebase_admin.initialize_app(cred)

registration_token = "cgjFTxdzg9212i3bjfnBmE:APA91bEgtqz6JeSliDSXSIHQ6lVg2xlYYLAiBFrTU7ujsY77yc7WhwXEP0kRTDMDrAha8V5XqAg_GRKH2A6eKgFigXUUaR0IrmVXWg24oMlTyo5GR1oe1zM"


message = messaging.Message(
    notification=messaging.Notification(
        title="Van Alert 🚐",
        body="The shuttle van has reached your department!"
    ),
    token=registration_token,
)

response = messaging.send(message)
print("✅ Successfully sent message:", response)
