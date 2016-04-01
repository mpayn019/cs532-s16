#Developed by Chevelle Taylor-Sakyi
import math
from math import *
import scipy
from scipy import stats
from scipy.spatial import distance

movies={}
linktable={}

correlation={}
#parse rating file
linkfile=open('data_files/u.data')
strline=linkfile.readlines()
for line in strline:
	uid,itemid,rating,_=line.split('\t')
	if uid not in linktable:
		linktable[uid]={}
	linktable[uid][itemid]=float(rating)
linkfile.close()
#parse movie file
moviefile=open('data_files/u.item')
strline=moviefile.readlines()
for line in strline:
	tuples=line.split('|')
	movies[tuples[0]]={'name' : tuples[1], 'wtotal':0, 'stoal':0, 'erate' : 0}
moviefile.close()

#calculate correlation
pickedId='37'
pickedUser=linktable[pickedId]
for uid in linktable :
	if uid==pickedId:
		continue
	pickedUserRating=[]
	currentUserRating=[]
	for mid in pickedUser:
		if linktable[uid].has_key(mid) :
			pickedUserRating.append(pickedUser[mid])
			currentUserRating.append(linktable[uid][mid])
	if len(currentUserRating)==0 :
		correlation[uid]=0
	else:
		correlation[uid]=scipy.stats.pearsonr(pickedUserRating,currentUserRating)[0]
		if not correlation[uid] or math.isnan(correlation[uid]) :
			correlation[uid]=float(1)/(float(1)+scipy.spatial.distance.euclidean(pickedUserRating,currentUserRating))
	#calculate estimated rating
	for mid in linktable[uid]:
		# ignore scores of zero or lower and only score movies I haven't seen yet
		if mid not in pickedUser and  correlation[uid]>0:
			movies[mid]['wtotal']+=linktable[uid][mid]*correlation[uid]
			movies[mid]['stoal']+=correlation[uid]
#calculate rating
for m in movies:
	if  movies[m]['stoal']!= 0:
		movies[m]['erate']=float(movies[m]['wtotal'])/float(movies[m]['stoal'])
	# if movies[m]['erate']>5 or movies[m]['erate']< -5:
	# 	print movies[m]
	

movieList=sorted(movies.values(),key=lambda v  : v['erate'],reverse=True)
print ('Top 5 recommendations for films')
for mv in movieList[:5]:
	print(mv['name']+'  Movie Rate: '+ str(mv['erate']))
print ('\nBottom 5 recommendations for films')
for mv in movieList[-5:] :
	print(mv['name']+'   Movie Rate:  '+ str(mv['erate']))