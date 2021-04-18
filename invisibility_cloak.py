import cv2
import numpy as np

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))

for i in range(60):
    ret, background = cap.read()


while (cap.isOpened()):
    ret, vid = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(vid, cv2.COLOR_BGR2HSV)

    #color ranges
    lower_red = np.array([0, 165, 70])
    upper_red = np.array([10, 255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 165, 70])
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    #bg mask
    mask1 = mask1 + mask2

    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    #inverse mask
    mask2 = cv2.bitwise_not(mask1)

    res1 = cv2.bitwise_and(vid, vid, mask=mask2)

    res2 = cv2.bitwise_and(background, background, mask=mask1)

    op = cv2.add(res1,res2)

    out.write(op)

    #cv2.imshow("mask2", mask2)
    #cv2.imshow("mask1", mask1)
    #cv2.imshow("res1", res1)
    #cv2.imshow("res2", res2)
    cv2.imshow("output", op)
 
    if cv2.waitKey(1)  & 0xFF == ord('q'):
      break

cap.release()
out.release()
cv2.destroyAllWindows()