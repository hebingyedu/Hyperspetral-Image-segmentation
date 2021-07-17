#coding=utf-8
from osgeo import gdal
import struct
import numpy as np
import os
import os.path
import cv2


class processRS:
    def __init__(self,filename,filetype=gdal.GDT_Float32):
        print("this program is programed by wangtf")
        self.filename=filename
        self.filetype=filetype
        self.dataset = gdal.Open(self.filename, gdal.GA_ReadOnly)
        if not self.dataset:
            print('Read file erro!')
        else:
            self.ShortName=self.dataset.GetDriver().ShortName
            self.LongName= self.dataset.GetDriver().LongName
            self.bandnum=self.dataset.RasterCount
            self.XSize=self.dataset.RasterXSize
            self.YSize=self.dataset.RasterYSize
            self.Projection=self.dataset.GetProjection()
            self.bandindex=range(1,self.bandnum+1)

    def Getparam(self):

        print("Driver: {}/{}".format(self.ShortName,
                             self.LongName))
        print("Size is {} x {} x {}".format(self.XSize,
                                    self.YSize,
                                    self.bandnum))
        print("Projection is {}".format(self.Projection))
    def getband(self,band,xoff, yoff,
                           xsize, ysize,
                           buf_xsize, buf_ysize):
        print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))
      
        min1 = band.GetMinimum()
        max1 = band.GetMaximum()
        if not min1 or not max1:
            (min1,max1) = band.ComputeRasterMinMax(True)
            print("Min={:.3f}, Max={:.3f}".format(min1,max1))
      
        if band.GetOverviewCount() > 0:
            print("Band has {} overviews".format(band.GetOverviewCount()))
      
        if band.GetRasterColorTable():
            print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))

        #此处gdal应该有bug，buf_xsize必须与buf_ysize相等，否则图像会花。。。。不清楚是不是只是这个版本
        #先用cv2缩放一下
        #print(buf_xsize)
        bufsize=max(buf_xsize,buf_ysize)
        scanimage = band.ReadRaster(xoff, yoff,
                           xsize, ysize,
                           bufsize, bufsize,
                           buf_type=self.filetype)
##        print('xsize',xsize)
##        print('ysize',ysize)
##        print('buf_xsize: ',buf_xsize)
##        print('buf_ysize: ',buf_ysize)
##        print(len(scanimage))
        tuple_of_floats = struct.unpack('f' * bufsize*(bufsize), scanimage)
        #a=np.asarray(tuple_of_floats)
        #print(a.max())
        result=np.zeros((bufsize,bufsize))
        result[:]=np.asarray(tuple_of_floats).reshape((bufsize,bufsize))
        result=cv2.resize(result,(buf_xsize,buf_ysize))
        #print('result shape',result.shape)
        return result     
        
    def GDALReadFile(self,bandindex,offx=0,offy=0,sizex=None,sizey=None,
                     scaleX=None,scaleY=None):
        if sizex==None:
            sizex=self.XSize
        if sizey==None:
            sizey=self.YSize
        if scaleX==None:
            scaleX=sizex
        if scaleY==None:
            scaleY=sizey
        databuf=[]
        for i in range(0,len(bandindex)):
            curband=self.dataset.GetRasterBand(bandindex[i])
            curbandbuf=self.getband(curband,offx,offy,sizex,sizey,scaleX,scaleY)[:]
            databuf.append(curbandbuf)
##            databuf=np.array(databuf)
##            databuf=databuf.transpose(1,2,0)
##            if(databuf.shape[2]==1):
##                databuf=databuf[:,:,0]
            
        return databuf
