import face_recognition


# 初始化已知人脸数据
def face_init_know_res(paths):
    known_faces = []
    known_faces_name = []
    for item in paths:
        known_face = face_recognition.load_image_file(item['path'])
        known_face_encoding = face_recognition.face_encodings(known_face)[0]
        known_faces.append(known_face_encoding)
        known_faces_name.append(item['name'])
    return known_faces, known_faces_name


# 初始化未知人脸数据（帧的方式）
def face_init_unknown_res(rgb_small_frame):
    unknow_face_locations = face_recognition.face_locations(rgb_small_frame)
    unknow_face_encodings = face_recognition.face_encodings(rgb_small_frame, unknow_face_locations)
    return unknow_face_encodings, unknow_face_locations


# 初始化未知人脸数据（文件图片的方式）
def face_init_unknown_res_file(file):
    unknow_face_locations = face_recognition.load_image_file(file)
    unknow_face_encodings = face_recognition.face_encodings(unknow_face_locations)[0]
    return unknow_face_encodings, unknow_face_locations


# 加载识别，返回识别后的人名
def face_use_test(known_faces, unknown_face_encoding, known_faces_name):
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    index = results.index(True)
    face_name = known_faces_name[index]
    return face_name