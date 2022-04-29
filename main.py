import cv2
import numpy as np

TOTAL_WIDTH = 800
TOTAL_HEIGHT = 600


def main():
    # Capturamos de la webcam
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, TOTAL_WIDTH)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, TOTAL_HEIGHT)

    while True:
        _, frame = webcam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_b = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        upper_b = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
        hsv = cv2.addWeighted(lower_b, 1.0, upper_b, 1.0, 0.0)
        kernel = np.ones((5, 5), np.uint8)
        hsv = cv2.erode(hsv, kernel)

        contours, _ = cv2.findContours(hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        approx = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            approx = cv2.approxPolyDP(cnt, 0.1 * cv2.arcLength(cnt, True), True)

            if area > 16000:
                print(approx[0][0][0])
                print(approx[0])
                cv2.drawContours(frame, [approx[0]], 0, (0, 0, 0), 10)
                cv2.drawContours(frame, [approx[1]], 0, (0, 0, 0), 20)

        cv2.rectangle(frame, (0, 0), (TOTAL_WIDTH, TOTAL_HEIGHT), (0, 255, 0), 3)
        cv2.rectangle(frame, (int(TOTAL_WIDTH/3), 0), (int((TOTAL_WIDTH/3)*2), TOTAL_HEIGHT), (0, 255, 0), 3)
        cv2.rectangle(frame, (0, int(TOTAL_HEIGHT/3)), (TOTAL_WIDTH, int((TOTAL_HEIGHT/3)*2)), (0, 255, 0), 3)
        if approx is not None:
            # print(len(approx))
            pass
        cv2.imshow('QR Detector', frame)
        cv2.imshow('Mask', hsv)

        if cv2.waitKey(1) == ord('q'):
            break
    webcam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
