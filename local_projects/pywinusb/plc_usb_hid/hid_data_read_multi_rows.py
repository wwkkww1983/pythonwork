data1 = [0, 62, 2, 2, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48]
data2 = [0, 62, 2, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48]
data3 = [0, 4, 2, 48, 3, 52, 51, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48,
         48, 48, 48, 48, 48, 48, 48, 48]

buffer = [data1, data2, data3]
newdata = [0 for i in range(3)]
newlen = 0
for n in range(len(buffer)):
    newlen += buffer[n][1]
    # if n == 0:
    #     # newdata += buffer[n][0:3]
    #     newdata += buffer[n][3:buffer[n][1]+3]
    #     # newdata.append(buffer[n][0:3])
    #     # newdata.append(buffer[n][3:buffer[n][1]])
    # elif 0 < n < len(buffer) - 1:
    #     newdata += buffer[n][3:buffer[n][1]+3]
    #     # newdata.append(buffer[n][3:buffer[n][1]])
    # elif n == len(buffer) - 1:
    #     # newdata.append(buffer[n][3:buffer[n][1]])
    newdata += buffer[n][3:buffer[n][1]+3]
newdata[:3] = [0, newlen, 2]
print(newlen, newdata)
print(newdata[:3], newdata[3:newdata[1]])
