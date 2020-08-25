import numpy as np
import obspy

def read_wave_data(station='afbi'):
    """
    read the wave height data
    :param        station: which station to read (default: 'afbi'):
    :return         times: times of the observations
    :return       wheight: wave heights at those times
    """

    # figure out which file to read
    fname=station+'.csv'
    print('Reading file '+fname)

    # open the file, just to get the first line this time
    fl=open(fname,'r')
    
    # read the header information
    ln = fl.readline()

    # close the file
    fl.close()

    # figure out which columns have the times and wave heights
    hdrs=ln.split(',')
    itime=np.where(['Time' in hdr for hdr in hdrs])[0][0]
    iheight=np.where(['Significant wave height' in hdr for hdr in hdrs])[0][0]


    # read the rest of the data, skipping the first line
    vls = np.loadtxt(fname,dtype=str,delimiter=',',skiprows=1,
                     usecols=[itime,iheight])

    # conver times to an obspy format
    times = np.array([obspy.UTCDateTime(tm) for tm in vls[:,0]])

    # grab the heights
    heights = vls[:,1]
    heights[heights==':']='NaN'
    heights[heights=='']='NaN'
    heights=heights.astype(float)

    

    return times,heights
