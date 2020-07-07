# Instruction
 data analysis

## cleaning data
load the datasets
looking through the data set

the number of contacts is decimal and has six digits after the decimal 
so that the unit of contacts is per million.
Two problems have been found:
1. It is abnormal that the value of visits is negative
2. It is weird that the number of visits is positive, whilst the number of contacts is equal to zero. 
In other words, people did not see the spots when they visit Trivago website.
To attempt to reveal reasons which cause this problem

split the column, spot, into 4 different columns including spot_id, 
spot_name, spot_length, and spot_campaign

## checking the structure
Based on the information, the quality of data is good 
In other words, there is no empty cell (NA) in the dataset#

There are 11 outliers in terms of cost per visit (CPV)
10 out of the 11 outliers results from the number of visits is zero, 
And one outlier is the result of that both the number of visits and the number of costs are equal to zero.
I will build up a new dataset, CPV_clear, in which the outliers have been removed.
The new dataset, CPV_clear, primarily focuses on the research regarding CPV.
I continue to apply the dataset, tv_spot_data when I study the visit per million contacts.
