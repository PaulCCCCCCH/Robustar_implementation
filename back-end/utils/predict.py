# 将预测结果转换为字符串
def convert_predict_to_string(output):
    result = str(float(output[0]))
    for i in range(1, len(output)):
        result += "_"+str(float(output[i]))
    return result
