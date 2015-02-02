# Introduction

The input data of the script were got form the original files:  
* 'train/X_train.txt': Training set
* 'train/y_train.txt': Training labels
* 'test/X_test.txt': Test set
* 'test/y_test.txt': Test labels
* 'features.txt': List of all features.
* 'activity_labels.txt': Links the class labels with their activity name.
* 'features_info.txt': Shows information about the variables used on the feature vector.
* 'train/subject_train.txt': Each row identifies the subject who performed the activity for each window sample. Its range is from 1 to 30. 
* 'test/subject_train.txt': Each row identifies the subject who performed the activity for each window sample. Its range is from 1 to 30. 

The output data files:  
"data_summary.txt": Including the data of the average of each variable for each activity and each subject, this is the output tidy data


# Approach of the script
1. Combining the training set 'x_train.txt' and test set 'y_test.txt' into a single data set
2. Extracting the column index set which include mean() or std() from the 'features.txt' file
3. Subsetting the data set with the got columns index set
4. Combining 'y_train.txt' and 'y_test.txt' into a single training labels list
5. Combining 'train/subject_train.txt' and 'test/subject_train.txt' into a single subject list
6. Combining the data set 3,4,5 into one single data set
7. Labeling the column in dataset 6 with the activity name from 'activity_labels.txt' file. This includes the required mean and standard deviation for each measurement.
8. Outputing the dataset into a file
9. Calculating the mean for every activity and every subject for each measurement variable
10. Combining all variables' mean into a single data frame. This is the required tidy data set with the average of each variable for each activity and each subject.
11. Outputing the data set in 10 into a second file


