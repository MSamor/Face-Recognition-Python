import cv2
import os
import numpy as np
import face_recognition
from scan_data_face import load_face_data_file
from face_recognition_init import face_init_know_res, face_init_unknown_res

PHOTO = "photo/face.jpg"

# 加载面部数据
def load_known_face(PTAH):
    # 加载已知人脸
    paths = load_face_data_file(PTAH)
    # 计算已知人脸
    know_face_encodings, konw_face_names = face_init_know_res(paths)
    return know_face_encodings, konw_face_names


# 运行OpenCv读取摄像头
def face_run(know_face_encodings, konw_face_names):
    global count
    process_this_frame = True
    video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            unknow_face_encodings, unknow_face_locations = face_init_unknown_res(rgb_small_frame)

            face_names = []
            for face_encoding in unknow_face_encodings:
                matches = face_recognition.compare_faces(know_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(know_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = konw_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(unknow_face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Camera', frame)
        k = cv2.waitKey(1)
        # 点击窗口关闭按钮退出程序
        if k == ord('s'):
            pic = cv2.resize(frame, (600, 400), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(PHOTO, pic)
            break
        if k == ord('q'):
            if os.path.exists(PHOTO):
                os.remove(PHOTO)
            break
        if cv2.getWindowProperty('Camera', 0) < 0:
            if os.path.exists(PHOTO):
                os.remove(PHOTO)
            break

    video_capture.release()
    cv2.destroyAllWindows()


