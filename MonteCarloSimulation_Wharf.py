# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:36:45 2016

@author: ojrussia
"""

from abaqus import *
from part import *
from section import *
from assembly import *
from job import *
from visualization import *
from connectorBehavior import *
import random
from odbAccess import *
from xlwings import Workbook, Range
import os
from numpy import*

#define model database

MyMdb=openMdb('Wharf_Randomization.cae')

#get workbook direction (assuming location is the same as this script)

direction=os.path.join(os.getcwd(),"Randomization.xlsm")

#if it's not, then use:
#direction="PathToFile/relevantExcelFile.xls"


#open the workbook

wb = Workbook(direction) 

#define first node of row (by number) (this is hard-coded based on the ABAQUS model)

indexList=[1,8,15,22,29,36,43,50,57,64,71,78,85,92,99,106,113,120,127,134]

#Define number of rows and columns (this is hard-coded based on the ABAQUS model)

nrows=20

ncols=7

#Define number of models (this is selected based on the desired number of simulations)

nmodels = 1000

#create new models

for i in range(1,nmodels+1):
    
    #initialize list of piles

    myList=[0]*140
    
    #shuffle list
    
    random.shuffle(indexList)
    
    #define model number
    
    model_num=str(i)
    
    #create new model from base model

    mdb.Model(name='Wharf_random', objectToCopy=
        mdb.models['Base'])
        
    #assign connector properties

    for j in range(0,nrows):
        
        for k in range(0,ncols):
        
            #link wire-set number to randomized list
        
            set_num = str(indexList[j]+k)
            
            #link section number to ordered list        
            
            section_num = str(ncols*(j)+k+1)
            
            #fill list of piles
            
            myList[ncols*(j)+k]=set_num
            
            #define model
        
            myModel = mdb.models['Wharf_random']
            
            #define wire-set
    
            mySet=myModel.rootAssembly.sets['Wire-'+set_num+'-Set-1']
            
            #assign section to wire-set
    
            myModel.rootAssembly.SectionAssignment(region=
                mySet, sectionName='P'+section_num)
              
    #print list to excel
            
    Range("Sheet1", "B"+model_num+":EK"+model_num).value = myList
    
    #create job
            
    mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
        SINGLE, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=
        'Wharf_random', modelPrint=OFF, multiprocessingMode=
        DEFAULT,name='Wharf_rand_'+model_num,nodalOutputPrecision=SINGLE, 
        numCpus=1,numDomains=1,parallelizationMethodExplicit=DOMAIN, scratch='', 
        type=ANALYSIS,userSubroutine='')
        
    #name the analysis job
        
    myJob = mdb.Job(name='Wharf_rand_'+model_num,model='Wharf_random')
    
    #submit the job

    myJob.submit()
    
    #wait for job completion
    
    myJob.waitForCompletion()
    
    #access output database

    mySession = session.openOdb(name='C:/Temp/Abaqus/OR/Wharf/New/Wharf_rand_'+model_num+'.odb')

    odb = session.odbs['C:/Temp/Abaqus/OR/Wharf/New/Wharf_rand_'+model_num+'.odb']
    
    #generate load proportionality factor data
    
    xy_result = session.XYDataFromHistory(name='LPF'+model_num, odb=odb, 
        outputVariableName='Load proportionality factor: LPF for Whole Model', 
        steps=('NonLinear_Buckling', ), )
    
    length_xy= len(xy_result)
    
    #extract collapse load proportionality factor
    
    for L in range (0,length_xy-1):
        if xy_result[L+1][1]-xy_result[L][1]>0:
            if xy_result[L+1][1]>0:
                if L+1==length_xy-1:
                    Range("Sheet1", "EM"+model_num).value = xy_result[L+1][1]
                else:
                    continue
            else:
                Range("Sheet1", "EM"+model_num).value = xy_result[L][1]     
        else:
            Range("Sheet1", "EM"+model_num).value = xy_result[L][1]
            break

#save excel sheet

wb.save("C:\\Temp\\Abaqus\\OR\\Wharf\\New\\Randomization.xlsm")
    