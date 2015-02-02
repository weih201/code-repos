## File name: datacleanPrj.R

## This file is the surce code for the Getting and Cleanning Data course project, which 
## is to address following tasks:

## 1.Merges the training and the test sets to create one data set.
## 2.Extracts only the measurements on the mean and standard deviation for each measurement. 
## 3.Uses descriptive activity names to name the activities in the data set
## 4.Appropriately labels the data set with descriptive variable names. 
## 5.Creates a second, independent tidy data set with the average of each variable for each activity and each subject. 

## Setting work directory
setwd("C:/my home/coursera/Data Science Specialization/getting and clean data/course project/UCI HAR Dataset")
list.files()

## Inout train and test data
dfTrain_X<-read.table("./train/X_train.txt")
dfTest_X<-read.table("./test/X_test.txt")
df_X<-rbind(dfTrain_X,dfTest_X)

## Read features and assign to data frame 
features<-read.table("features.txt",stringsAsFactors=FALSE)
colnames(df_X)<-features$V2

## Select the mean and standard deviztion cols and subsetting original data set
keep<-grepl("mean\\(\\)|std\\(\\)", names(df_X), ignore.case = TRUE)
dfx_Keep<-df_X[, keep] 

## Read the activity labels
labels<-read.table("activity_labels.txt")

## Read the subject and training data set for each activity
sub_train<-read.table("./train/subject_train.txt")
train_y<-read.table("train/Y_train.txt")
sub_test<-read.table("test/subject_test.txt")
test_y<-read.table("test/Y_test.txt")

## df is the data frame which combine the subject, activity and the measurement
## Every row in df corresponds to a activity
df<-data.frame(rbind(sub_train,sub_test),rbind(train_y,test_y),dfx_Keep)
names(df)<-c("Subject","Activity",names(dfx_Keep))

## Labeling the activity with info from the activity labels file
df_merge<-merge(df,labels,by.x="Activity",by.y="V1",all.x=TRUE,sort=FALSE)
df_merge<-data.frame(df_merge$V2,df_merge[,-c(1,ncol(df_merge))])
names(df_merge)<-c("Activity","Subject",names(dfx_Keep))
## Re-arrange the get data set df_merge as the [Subject, Activity, Measurment] form
df_merge<-df_merge[c(2,1,3:ncol(df_merge))]

## Group the data with subject
o<-order(df_merge$Subject,df_merge$Activity)
## Final Extracted data set
df_merge<-df_merge[o,]
## Output it to a file
write.table(df_merge, "mean_std.txt", sep="\t")

## Get the the average of each variable for each activity and each subject
## The col 3 is the first valid measurement
library("reshape2")
dfm<-melt(df_merge, id=c("Subject","Activity"))
#use dcast to create the final, tidy, data set.
# ominious function uesed to calcualte mean
dfmean <-  dcast(dfm, Subject + Activity ~ variable, function(x)sum(x)/length(x))   
## Output it into a file
write.table(dfmean, "data_summary.txt", sep="\t",row.name=FALSE )
