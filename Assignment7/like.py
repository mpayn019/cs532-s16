#Developed by Chevelle Taylor-Sakyi
import math
from math import *
import scipy
from scipy import stats
from scipy.spatial import distance
users={}
movies={}
linktable={}

correlation={}
def recommandate(pid):
	correlation={}
	pickedMovie=linktable[pid]
	for mid in linktable :
		if mid==pid:
			continue
		pickedMovieRating=[]
		currentMovieRating=[]
		for uid in pickedMovie:
			if  uid in linktable[mid] :
				pickedMovieRating.append(pickedMovie[uid])
				currentMovieRating.append(linktable[mid][uid])
		if len(currentMovieRating)==0 :
			correlation[mid]=0
		else:
			correlation[mid]=scipy.stats.pearsonr(pickedMovieRating,currentMovieRating)[0]
			if not correlation[mid] or math.isnan(correlation[mid]) :
				correlation[mid]=float(1)/(float(1)+scipy.spatial.distance.euclidean(pickedMovieRating,currentMovieRating))
	correlationArray=sorted(correlation,key=correlation.get,reverse=True)
	print('Top 5 most correlated movies:')
	for m in  correlationArray[:5] :
		print(movies[m] +'  ( correlation: '+str(correlation[m])+' ) ')

	print('Bottom 5 least correlated movies:')
	for m in correlationArray[-5:] :
		print(movies[m]+' ( correlation: '+str(correlation[m])+' ) ')

#parse rating file
linkfile=open('data_files/u.data')
strline=linkfile.readlines()
for line in strline:
	uid,itemid,rating,_=line.split('\t')
	if itemid not in linktable:
		linktable[itemid]={}
	linktable[itemid][uid]=float(rating)
linkfile.close()
#parse movie file
moviefile=open('data_files/u.item')
strline=moviefile.readlines()
for line in strline:
	tuples=line.split('|')
	movies[tuples[0]]=tuples[1]
moviefile.close()

#calculate correlation
pickedId='50'
print('Favorite movie: 50|Star Wars (1977)')
recommandate(pickedId) 

print
print('Least favorite movie: 254|Batman & Robin (1997)')
pickedId='254'
recommandate(pickedId)