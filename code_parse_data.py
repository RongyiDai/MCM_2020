import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_total = pd.DataFrame()
df_summer_total = pd.DataFrame()

# parse data into a list of lists
for file in range(2004, 2020):
	filename = str(file)+".txt" 
		 # print(os.path.join(directory, filename))
	file_obj_read = open(filename, 'r')
	list1 = []
	i = 0;
	for line in file_obj_read:
		line.strip()
		innerList = [];
		line2 = line.split()
		for word in line2:
			firstPosition = word.find("-32768")
			lastPosition = word.rfind("-32768")
			#in the case that in that specific line we have no instance of the repitition
			if (firstPosition == -1): 
				innerList.append(int(word))
			else:
				#find out the number up and until the -32768 comes up
				num1 =   word[0:firstPosition] 
				innerList.append(num1)
				forLoopIterations = int((lastPosition - firstPosition)/6)
				for i in range(0, forLoopIterations):
					innerList.append(-32768)
				innerList.append(-32768)
		list1.append(innerList)


	for list2 in list1:
		if list2[0] == "":
			list2.pop(0)

	
	file_obj_read.close()

	ori_array = np.array(list1).astype(int)
	
	print(ori_array.shape)

	# yearly temperature data of the 15 grid
	df_yearly = pd.DataFrame()
	summer_list = []
	for i in range(12):
		print("********** Month: "+ str(i+1) + "***********")
		j = 24 + i*180
		k = 39 + i*180
		target = ori_array[j:k, 160:185]
		average_list = []
		df_monthly = pd.DataFrame()
		index = ["51-56`N, 20-15'W", "51-56`N, 15-10'W","51-56`N, 10-5'W","51-56`N, 5-0'W","51-56`N, 0--5'W", 
		"56-61`N, 20-15'W", "56-61`N, 15-10'W","56-61`N, 10-5'W","56-61`N, 5-0'W","56-61`N, 0--5'W",
		"61-66`N, 20-15'W", "61-66`N, 15-10'W","61-66`N, 10-5'W","61-66`N, 5-0'W","61-66`N, 0--5'W"]
		
		columns = [str(file)+"/"+str(i) for i in range(1, 13)]
		
		# calculating average temperature of the 15 grids
		for x in range(3):
			for y in range(5):
				print("-------" +str(51+x*5)+"-"+str(51+(x+1)*5)+"`N, "+ str(20-y*5)+"-"+str(20-(y+1)*5)+"`W -----------") 
				grid = target[(x*5):(5+x*5), (y*5):(5+y*5)]
				grid_water_only = []
				for g in grid:
					grid_water_only.extend([e for e in g if e != -32768])
					
				average = sum(grid_water_only)/(100*len(grid_water_only))
				
				print(average)
				average_list.append(average)
				
		df = pd.DataFrame(average_list)
		# monthly data of the 15 grids
		df_monthly = pd.concat([df_monthly, df], axis = 1)

		df_yearly = pd.concat([df_yearly, df_monthly], axis = 1)
	
	df_yearly.columns = columns
	df_yearly.index = index
	
	# yearly data for all of the grids
	df_total = pd.concat([df_total, df_yearly], axis = 1)
	df_total.to_excel("temperature_time.xlsx")

# plot the temperature over 15 years for each of the grid
for i in range(15):

	plt.plot(label, temp_list[i])
	plt.title(list(df_summer_total.index)[i])
	plt.show()



	
	
 
  
