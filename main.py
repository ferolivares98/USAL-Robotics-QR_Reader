import cv2
import numpy as np

TOTAL_WIDTH = 800
TOTAL_HEIGHT = 600
X_IZQ = TOTAL_WIDTH - 550
X_DER = TOTAL_WIDTH - 250
Y_ARRIBA = TOTAL_HEIGHT - 450
Y_ABAJO = TOTAL_HEIGHT - 150


def main():
    # Capturamos de la webcam
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, TOTAL_WIDTH)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, TOTAL_HEIGHT)
    pos = 0

    while True:
        _, frame = webcam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Estricto
        # lower_b = cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        # upper_b = cv2.inRange(hsv, (160, 100, 100), (179, 255, 255))
        # Menos estricto
        lower_b = cv2.inRange(hsv, (0, 80, 80), (10, 255, 255))
        upper_b = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))

        hsv = cv2.addWeighted(lower_b, 1.0, upper_b, 1.0, 0.0)
        kernel = np.ones((5, 5), np.uint8)
        hsv = cv2.erode(hsv, kernel)

        contours, _ = cv2.findContours(hsv, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 16000:
                approx = cv2.approxPolyDP(cnt, 0.2 * cv2.arcLength(cnt, True), True)
                if len(approx) == 2:
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                    pos = calculo_pos(approx, pos, area)
                    break

        cv2.rectangle(frame, (0, 0), (TOTAL_WIDTH, TOTAL_HEIGHT), (0, 255, 0), 3)
        # Detección cuadrada
        cv2.rectangle(frame, (0, Y_ARRIBA), (TOTAL_WIDTH, Y_ABAJO), (0, 255, 0), 3)
        cv2.rectangle(frame, (X_IZQ, 0), (X_DER, TOTAL_HEIGHT), (0, 255, 0), 3)
        # Detección rectangular
        # cv2.rectangle(frame, (int(TOTAL_WIDTH/3), 0), (int((TOTAL_WIDTH/3)*2), TOTAL_HEIGHT), (0, 255, 0), 3)
        # cv2.rectangle(frame, (0, int(TOTAL_HEIGHT/3)), (TOTAL_WIDTH, int((TOTAL_HEIGHT/3)*2)), (0, 255, 0), 3)

        cv2.imshow('QR Detector', frame)
        cv2.imshow('Mask', hsv)

        if cv2.waitKey(1) == ord('q'):
            break
    webcam.release()
    cv2.destroyAllWindows()


def calculo_pos(puntos, pos, area):
    """
    Puntuamos las posiciones de 1 a 9. Así evitamos imprimir continuamente si no hay cambio de movimiento.
    Utilizamos el 10 para la distancia.
    """
    # Centro.
    # Posición principal. Correctamente centrado.
    if puntos[0][0][0] > X_IZQ and puntos[0][0][1] > Y_ARRIBA \
            and puntos[1][0][0] > X_IZQ and puntos[1][0][1] > Y_ARRIBA \
            and puntos[0][0][0] < X_DER and puntos[0][0][1] < Y_ABAJO \
            and puntos[1][0][0] < X_DER and puntos[1][0][1] < Y_ABAJO:
        if area < 24000:
            if pos != 10:
                print("Avanzar hacia adelante.")
                separador_inst()
            return 10
        if pos != 5:
            print("OK. Quieto.")
            separador_inst()
        return 5

    # Centrado pero...
    if puntos[0][0][0] > X_IZQ and puntos[1][0][0] < X_DER:
        # Arriba.
        if puntos[0][0][1] < Y_ARRIBA or puntos[1][0][1] < Y_ARRIBA:
            if pos != 2:
                comprobar_area(area)
                print("Avanzar hacia abajo.")
                separador_inst()
            return 2
        # Abajo.
        if puntos[0][0][1] > Y_ABAJO or puntos[1][0][1] > Y_ABAJO:
            if pos != 8:
                comprobar_area(area)
                print("Avanzar hacia arriba.")
                separador_inst()
            return 8

    # Escorado a la izquierda (vista de pantalla, inversa de las instrucciones).
    if puntos[0][0][0] < X_IZQ or puntos[1][0][0] < X_IZQ:
        # Arriba izquierda.
        if puntos[0][0][1] < Y_ARRIBA or puntos[1][0][1] < Y_ARRIBA:
            if pos != 1:
                comprobar_area(area)
                print("Avanzar hacia abajo e izquierda.")
                separador_inst()
            return 1
        # Abajo izquierda
        elif puntos[0][0][1] > Y_ABAJO or puntos[1][0][1] > Y_ABAJO:
            if pos != 7:
                comprobar_area(area)
                print("Avanzar hacia arriba e izquierda.")
                separador_inst()
            return 7
        # Izquierda
        else:
            if pos != 4:
                comprobar_area(area)
                print("Avanzar hacia la izquierda.")
                separador_inst()
            return 4

    # Escorado a la derecha.
    if puntos[0][0][0] > X_DER or puntos[1][0][0] > X_DER:
        # Arriba derecha.
        if puntos[0][0][1] < Y_ARRIBA or puntos[1][0][1] < Y_ARRIBA:
            if pos != 3:
                comprobar_area(area)
                print("Avanzar hacia abajo y derecha.")
                separador_inst()
            return 3
        # Abajo derecha.
        elif puntos[0][0][1] > Y_ABAJO or puntos[1][0][1] > Y_ABAJO:
            if pos != 9:
                comprobar_area(area)
                print("Avanzar hacia arriba y derecha.")
                separador_inst()
            return 9
        # Derecha.
        else:
            if pos != 8:
                comprobar_area(area)
                print("Avanzar hacia la derecha.")
                separador_inst()
            return 8

    return 0


def comprobar_area(area):
    # Tamaño insuficiente.
    if area < 25000:
        print("Avanzar hacia adelante y...")


def separador_inst():
    print("---------------------------------------")


if __name__ == '__main__':
    main()
