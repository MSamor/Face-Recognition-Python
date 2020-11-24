import os


# 加载文件
def load_face_data_file(path):
    pathsDic = []
    filePath = [os.path.join(path, f) for f in os.listdir(path)]
    for itemPath in filePath:
        tempFileName = itemPath.split("\\")[-1]
        tempFilePath = itemPath
        tempPerName = itemPath.split("\\")[-1].split(".")[0]
        pathsDic.append({"path": tempFilePath, "imgName": tempFileName, "name": tempPerName})
    return pathsDic


# 加载文件递归方式（本程序未使用）
def load_face_data_tra(path):
    def traverse(path, pathsDic):
        tempFilePath = ''
        tempFileName = ''
        tempPerName = ''
        filePath = [os.path.join(path, f) for f in os.listdir(path)]
        for itemPath in filePath:
            if os.path.isdir(itemPath):
                traverse(itemPath, pathsDic)
            elif os.path.isfile(itemPath):
                if itemPath.split("\\")[-1].split(".")[0][-4:] == '0001':
                    tempFileName = itemPath.split("\\")[-1]
                    tempFilePath = itemPath.split("\\")[0] + "/" +itemPath.split("\\")[1]+"/" +itemPath.split("\\")[2]
                    tempPerName = itemPath.split("\\")[1]

        pathsDic.append({"path":tempFilePath, "imgName":tempFileName,"name":tempPerName})
        return tempFilePath, tempFileName, tempPerName
    result = []
    traverse(path, result)
    del result[-1]
    return result