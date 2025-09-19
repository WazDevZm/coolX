import os
import cv2

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    
number_of_classes = 3
dataset_size = 100
# we building and delying code

def is_imshow_supported():
    try:
        cv2.namedWindow("test")
        cv2.imshow("test", cv2.imread(os.path.join(DATA_DIR, os.listdir(DATA_DIR)[0]) if os.listdir(DATA_DIR) else None))
        cv2.destroyWindow("test")
        return True
    except Exception:
        return False

cap = cv2.VideoCapture(0)
if not is_imshow_supported():
    print("Error: OpenCV is not built with GUI support (cv2.imshow is unavailable). Please install the correct opencv-python package and ensure your environment supports GUI operations.")
    cap.release()
    exit(1)

for j in range(number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))
    print('Collecting data for class {}' .format(j))

    done = False
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) == ord('q'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)
        counter += 1

cap.release()
cv2.destroyAllWindows()