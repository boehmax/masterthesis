#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import matplotlib.pyplot as plt
import os.path
import numpy as np
import re
import matplotlib.patches as mpatches


# In[15]:


path = "C:\\Users\\boehm\\FAUbox\\MA\\data\\lcms\\ms\\profils\\"


# In[16]:


paths=[]
os.chdir(path)
for DIR in os.listdir('.'): #to get folder
    if not os.path.isdir(DIR):
        pass
    else:
        os.chdir(DIR)
    for FILE in os.listdir('.'): #to get file
        if FILE.endswith(".csv"):
            filei = str(path+ DIR +'\\'+FILE)
            paths.append(filei) #paths is list of paths to all .csv-files
            FILE2=FILE.replace('.csv','') #variable that can be used for naming plot
            #print(DIR+'_'+FILE2)
        else:
            pass
    
    os.chdir(path)


# In[23]:


for STEP in paths:
    STEP2=STEP.replace(path,'')
    df = pd.read_csv(STEP, skiprows=[1], header=0, names=['x','y'])
    da = pd.DataFrame(df)
    med=da['y'].median() # MEDIAN
    thresh = 10*med
    distance = 10
    d1 = da[:][da['y']> thresh] #creates matrix with only the peaks and x with correct threshold
    da['labels'] = d1['x']
    da['labels'].astype(str)
    labels = da['labels'].tolist()
        #print(np.isnan(labels))
    for index, label in enumerate(labels): #creates a list of 0 and 1. 1 == above threshold, 0==below. the list is then mutliplied to to elimnate every peak below the set threshold.
        if np.isnan(label):
            labels[index] = 0
        else:
            labels[index] = 1

    df1 = da['y']*labels

    labels_height = df1.tolist()
   
    for index, height in enumerate(labels_height):#this for loop will eliminate near peaks, set distance above high to get only very high peaks without their neighbours
        for i in range(distance):   #this for loop will iterate over the number saved as distance to kill the nerast, the second nersat ... the "distance"nd nearest peak that is smaller          
            if labels_height[index] < labels_height[index-i]:
                labels_height[index] = 0
            else: 
                if labels_height[index-i] < labels_height[index]:
                    labels_height[index-i] = 0

    for index, height in enumerate(labels_height): #converts the list i just generated to list of 0 and 1 so i can multipy with labes generated above, only the ones are kept that are okay with the distance function
        if labels_height[index] > 0:
            labels_height[index] = 1
                  
            
    da['new_label'] = da['labels']*labels_height                    
    d2 = da[:][np.isfinite(da['new_label']) & da['new_label'] != 0] #creates a data frame with only the labes i want, with x values for the xtics

    #START: GETTING THE TIME as a STRING FOR LEGEND
    STEP2=STEP.replace(path,'')
    print(STEP2)
    STEP3 = re.sub(r'^.*?S', 'S', STEP2)
    PREHOUR = re.search('_(.*)_', STEP3)
    HOUR = PREHOUR.group(1)
    PREMINUTE = STEP2[STEP2.rindex('_')+1:]
    MINUTE= PREMINUTE.replace('.csv','')
    TIME = HOUR+'.'+MINUTE+' min'
    #END
    #START: GETTING TITLE
    STEP4 = STEP2.replace('\\'+STEP3,'')
    STEP5 = STEP4[9:]
    STEP6 = STEP5.replace('_',' ')
    STEP7 = STEP3[:2]
    if STEP7 == 'S1':
        STEP7 = 'ESI-'
    if STEP7 == 'S2':
        STEP7 = 'ESI+'
    STEP8 = STEP2.replace('\\','_')
    
    #### Plot
    
    fig = plt.figure(figsize=(12,3))
    ax = plt.subplot()
    da2 = med < da['y']
    da3 = da2 * da['y']
    plt.bar(da['x'], da3, width=2)
    #plt.bar(da['x'],da['y'],width= 2) #PEAK WIDTH BELOW 0.8 not visible
    #X = list(da.iloc[:, 0])
    #Y = list(da.iloc[:, 1])
    # Plot the data using bar() method
    #plt.bar(X, Y, color='g')
    plt.ylim(med,)
    plt.title(STEP6)
    plt.xlabel("Ion [m/z]")
    plt.ylabel("Intensity [counts]")
    plt.text(0.9,0.9, TIME, transform = ax.transAxes)
    plt.text(0.9,0.8, STEP7, transform = ax.transAxes)
    ax2 = plt.twiny()
    ax2.set_xticks(ticks= da['x'])
    ax2.xaxis.grid(True, linestyle = '-', linewidth=0.2)
    plt.xticks(rotation=90, ticks=d2['x'], labels=d2['new_label'].tolist())
    ax2.set_xlabel('', color='r')
    ax2.bar(da['x'], da3, width=2)
    ax2.tick_params('x', colors='k')
    plt.savefig(STEP8+".svg", format="svg")
    
    
# Show the plot
    plt.show()
    


# In[28]:


print(d2)


# In[ ]:





# In[ ]:




