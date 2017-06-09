from pymouse import PyMouse
import time
#鼠标操作	
for i in range(500):
    m=PyMouse()
    mp=[329,445]
    mrc=[428,491]
    mlc=[1144,477]
    mln=[600,443]
    #mp = m.position()	#获取光标位置
    #print(mp)
    #m.move(mp[0],mp[1])	#光标移动至坐标
    m.click(mp[0],mp[1],2)
    time.sleep(.4)
    m.click(mrc[0],mrc[1])
    time.sleep(.4)
    m.click(mlc[0],mlc[1])
    time.sleep(.4)
    m.click(mln[0],mln[1])
    time.sleep(.4)

