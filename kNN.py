from numpy import *
import operator
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A',' B','B']
    return group,labels
def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffmat=diffMat**2
    sqdistances=sqDiffmat.sum(axis=1)
    distances=sqdistances**0.5
    sortedDistIndeicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndeicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
        sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


def file2matirx(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))

    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector
def autonorm(dataSet):
    minvals=dataSet.min(0)
    maxvals=dataSet.max(0)
    ranges=maxvals-minvals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minvals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minvals

def datingClassTest():
    hoRatio=0.1

    datingDataMat,datingLabels=file2matirx('datingTestSet2.txt')
    normMat,ranges,minVals=autonorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print('the classifier came back with :%d,the real answer is :%d' %(classifierResult,datingLabels[i]))
        if classifierResult!=datingLabels[i]:
            errorCount+=1
    print(numTestVecs)
    print('error rate is :%f'%(errorCount/float(numTestVecs)))

def img2vector(filename):
    returnvect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnvect[0,32*i+j]=int(lineStr[j])
    return returnvect
def handWritingClassTest():
    hwLabels=[]
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNmaeStr=trainingFileList[i]
        fileStr=fileNmaeStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector('trainingDigits/%s' % fileNmaeStr)
    testFileList=listdir('testDigits')

    errorCount=0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        print(fileStr,fileNameStr.split('.'))
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2vector('testDigits/%s' % fileNameStr)
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,3)

        print('the classifier came back with %d,the real anser is %d' % (classifierResult,classNumStr))
        if classifierResult!=classNumStr:
            errorCount+=1
    print('error number is %d' %errorCount)
    print('error rate %f' % (errorCount/float(mTest)))