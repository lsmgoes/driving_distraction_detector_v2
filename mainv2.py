# !pip install opencv-python mediapipe ultralytics
# Para execução em GPU é necessário importar o CUDA
# Versão refatorada com aplicação de conceitos de STR
import cv2
import mediapipe as mp
import math
import time
import threading
from ultralytics import YOLO
import winsound

# Configurações Iniciais
PERIODO = 1 / 30  # 30 FPS
RESOLUCAO = (1280, 740)
LIMIAR_OLHO = 12
TEMPO_FECHADO = 2  # segundos

# Inicializações
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
modelo = YOLO("yolov8n.pt")
faceMesh = mp.solutions.face_mesh.FaceMesh()

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

# Variáveis Globais
controleAlarme = False
controleAlarmeSono = False
situacao = ""
tempo = 0
status = ""
inicio = time.time()

# Funções de Alarme
def alarme():
    global controleAlarme
    controleAlarme = True
    winsound.Beep(2000, 1000)
    time.sleep(1)
    controleAlarme = False

def alarmeSono():
    global controleAlarmeSono
    controleAlarmeSono = True
    winsound.Beep(2000, 1000)
    time.sleep(1)
    winsound.Beep(2000, 1000)
    controleAlarmeSono = False

# Função de Detecção de Celular
def identificarCelular(img):
    resultado = modelo(img, verbose=False)

    for objetos in resultado:
        for dados in objetos.boxes:
            x, y, w, h = map(int, dados.xyxy[0])
            conf = float(dados.conf[0])
            cls = int(dados.cls[0])

            if cls == 67 and conf > 0.5:
                return [x, y, w, h]

    return []

# Thread: Processamento Facial
def processar_face(img, results):
    global status, situacao, tempo, inicio

    h, w, _ = img.shape

    for face in results.multi_face_landmarks:
        distDiPx = math.hypot(
            int(face.landmark[159].x * w) - int(face.landmark[145].x * w),
            int(face.landmark[159].y * h) - int(face.landmark[145].y * h)
        )

        distEsPx = math.hypot(
            int(face.landmark[386].x * w) - int(face.landmark[374].x * w),
            int(face.landmark[386].y * h) - int(face.landmark[374].y * h)
        )

        if distEsPx <= LIMIAR_OLHO and distDiPx <= LIMIAR_OLHO:
            situacao = 'F'

            if status != situacao:
                inicio = time.time()
        else:
            situacao = 'A'
            inicio = time.time()
            tempo = 0

        if situacao == 'F':
            tempo = round(time.time() - inicio, 1)

        status = situacao

        if tempo >= TEMPO_FECHADO and not controleAlarmeSono:
            threading.Thread(target=alarmeSono).start()

# Loop Principal
while True:
    ciclo_inicio = time.time()

    ret, img = video.read()

    if not ret:
        break

    img = cv2.resize(img, RESOLUCAO)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = faceMesh.process(imgRGB)

    celular = identificarCelular(img)

    if celular:
        cv2.rectangle(
            img,
            (100, 100),
            (405, 150),
            (0, 0, 255),
            -1
        )

        cv2.rectangle(
            img,
            (celular[0], celular[1]),
            (celular[2], celular[3]),
            (0, 0, 255),
            5
        )

        cv2.putText(
            img,
            'ALERTA! CELULAR',
            (105, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

        if not controleAlarme:
            threading.Thread(target=alarme).start()

    else:
        cv2.rectangle(
            img,
            (100, 100),
            (370, 150),
            (0, 255, 0),
            -1
        )

        cv2.putText(
            img,
            'SEM CELULAR',
            (105, 135),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

    if results and results.multi_face_landmarks:
        threading.Thread(
            target=processar_face,
            args=(img, results)
        ).start()

    if not controleAlarmeSono:
        cv2.rectangle(
            img,
            (100, 30),
            (370, 80),
            (0, 255, 0),
            -1
        )

        cv2.putText(
            img,
            'ACORDADO',
            (105, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

    else:
        cv2.rectangle(
            img,
            (100, 30),
            (405, 80),
            (0, 0, 255),
            -1
        )

        cv2.putText(
            img,
            'ALERTA! DORMINDO',
            (105, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            3
        )

    cv2.imshow('img', img)

    if cv2.waitKey(1) == 27:
        break

    # Controle temporal do ciclo
    tempo_execucao = time.time() - ciclo_inicio

    if tempo_execucao < PERIODO:
        time.sleep(PERIODO - tempo_execucao)

# Finalização
video.release()
cv2.destroyAllWindows()