import numpy as np
import cv2
def showRGB(img_r,img_g,img_b,a):
    im=[]
    im.append(img_r)
    print(img_r.shape)
    print('imgr:min=%,max=%',img_r.min(),img_r.max())
    im.append(img_g)
    print('imgr:min=%,max=%',img_g.min(),img_g.max())
    im.append(img_b)
    im=np.array(im)
    print('imgr:min=%,max=%',img_b.min(),img_b.max())
    im=im.transpose(1,2,0)
    print(im.shape)
##    cv2.imshow('test',im)
##    cv2.waitKey(0)
##    cv2.destroyAllWindows()  
    return im
