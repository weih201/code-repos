omp90049 proj2 includes the "KTProject2.jar" file, "stopwords.txt" and "src" subdirectory.

The "src" directory include the source code for this projects. It includes three files: "TextClassifier.java", "WekaClassifier.java" and "Stemmer.java".

"TextClassifier.java" includes TextClassifier class and two inner classes: FileClass and StemItem.

TextClassifier class is sytem starting class. The text features extracting code located in this class. This class also invoking WekaClassifer's method to do the text classification. 

The FileClass and StemItem are two assistant classes to store the file and item relative info.

WekaClassifier is interface class to Weka package. The system invoking its methods to invoke Weka service.

"Stemmer.java" file copy from Porter stemmer's code. It is used to stem the words.

"stopwords.txt" file contains the stopwords list used in text features extracting. It should be located in the same directory as the *.class files.

To complie them: 
	javac -classpath weka.jar path *.java

To run them: java -classpath weka path TextClassifier  train.class dev.class

For I alrady creating the KTProject2.jar file.  A simple way to run the program is:
	java -jar  KTProject2.jar  train.class dev.class


The classification result stored in "results.class" file. It has the same form as "train.class".


The system always assume the real text files are stored in the subdirectory such as "\train" for "train.class", "\dev" for "dev.class".

For the providing trainnig files in "\train" and testing files "\dev", the program need run about 10minutes.
