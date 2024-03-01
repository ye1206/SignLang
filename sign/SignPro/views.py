from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import cv2
import mediapipe as mp
import time
from PIL import Image


def homePage(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def trackingTest(request):
    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands  # 模型選擇 hands

    hands = mpHands.Hands(min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
    mpDraw = mp.solutions.drawing_utils
    handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
    handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)
    pTime = 0
    cTime = 0

    while True:
        ret, img = cap.read()
        if ret:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result = hands.process(imgRGB)

            # print(result.multi_hand_landmarks)
            imgHeight = img.shape[0]
            imgWidth = img.shape[1]

            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    mpDraw.draw_landmarks(
                        img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                    for i, lm in enumerate(handLms.landmark):
                        xPos = int(lm.x * imgWidth)
                        yPos = int(lm.y * imgHeight)

                    # cv2.putText(img, str(i), (xPos-25, yPos+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 2)

                    # if i == 4:
                    #     cv2.circle(img, (xPos, yPos), 20, (166, 56, 56), cv2.FILLED)
                    # print(i, xPos, yPos)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, f"FPS : {int(fps)}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            # cv2.imshow('img', img)

            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

            # 將 PIL 圖像轉換為 JPEG
            response = HttpResponse(content_type="image/jpeg")
            img_pil.save(response, "JPEG")

            if cv2.waitKey(1) == ord('q'):
                break

        return response
