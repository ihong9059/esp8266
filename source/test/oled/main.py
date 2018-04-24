import os
from dispOled import dispOled
dispList = ['20180425','UTTEC','Hong K.S','Start']
print('Files:{}'.format(os.listdir()))

dispOled(dispList)
print('End of Test')
