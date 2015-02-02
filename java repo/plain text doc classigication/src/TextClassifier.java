/*
 * Wei Han's New File
 *  Created on 19/05/2012
 */
import java.io.File;
import java.io.PrintWriter;
import java.io.FileOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Collections;
import java.util.Set;
import java.util.TreeSet;
import java.util.Iterator;

import weka.core.SparseInstance;

public class TextClassifier {

	static String trainClass, devClass;
	static String stopWordsFile;
	static String resultsFile;
	static String logFile;
	static String trainArff;
	static String devArff;
	static boolean evalMode;
	
	static Stemmer stemmer = new Stemmer();
	static int freqTh = 1;
	static int featureLen = 200; //Maximum features length for each genre
	static Set<String> featureWords = new TreeSet<String>();
	static ArrayList<StemItem> featureItems = new ArrayList<StemItem>();
	
	static ArrayList<StemItem> itemFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> AFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> BFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> CFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> DFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> EFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> FFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> GFreqList = new ArrayList<StemItem>();
	static ArrayList<StemItem> HFreqList = new ArrayList<StemItem>();
	
	ArrayList<FileClass> trainList = new ArrayList<FileClass>();
	ArrayList<FileClass> devList = new ArrayList<FileClass>();
	ArrayList<String> stopWordsList = new ArrayList<String>();
	
	static PrintWriter outputStream = null;
 
	public static void main(String[] args) {
		if(args.length==2){  // check input parameters length
			trainClass = args[0];  // train class
			devClass = args[1];
		}
		else{
			System.out.println("Usage: java TextClassifer trainClass devClass ");
			System.exit(0);
 		}
		
//		trainClass = "train.class";
//		devClass = "dev.class";
		stopWordsFile = "stopwords.txt";
		resultsFile = "results.class";
		
		logFile = "log.dat";
		trainArff = "train.arff";
		devArff = "dev.arff";
		
		evalMode = false;
		
		try
		{
			outputStream = new PrintWriter(new FileOutputStream(logFile));
		}
		catch(FileNotFoundException e)
		{
			System.out.println("Error opening the logFile.");
			return;
		}

		TextClassifier tc = new TextClassifier();
		tc.start();
	}

/**
 *  start() control the process of the features extract
 *  1: it read the input file list and creating FileClass list with inputClassFiles
 *  2: invoking inputFiles to retrieve every file in the list and transforming them into 
 *     the stem list and storing them into the FileClass item
 *  3: freqCount: creating general and class stem frequency list
 *  4: coefFreq: adjusting class stem freq value base on their difference to general freq
 *  5: sortingList: sorting the class freq list 
 *  6: featureWordsCreating: creating the general features list base on the class freq list
 *  7: featuringFiles: featuring ever file base on general feature list
 *  
 */
	public void start(){
		startTrainning();
		
		devFeature();
		
		classifying(trainArff,devArff);
	}
	
	public void classifying(String trainFile, String testFile){
		WekaClassifier classifier = new WekaClassifier(trainFile,testFile);
		
		try{
			classifier.creatInstance();
		}
		catch(Exception e){
			System.out.println("Fail to create instance");
			System.out.println(e.toString());
		}
		
		try{
			classifier.setNBC();
		}
		catch(Exception e){
			System.out.println("Fail to set classifier");
			e.printStackTrace();
			System.out.println(e.getMessage());
		}
			
		try{
			classifier.buildModel(evalMode);
			if(evalMode){
				System.out.println(classifier.toString());
			}
		}
		catch (Exception e){
			System.out.println("build() error");
			e.printStackTrace();
			System.out.println(e.getMessage());
		}
		
		if(!evalMode){
			try{
				classfyTestInstances(devList,classifier);
				outClassifyResults(devList);
				System.out.println("The classification is finished");
			}
			catch (Exception e){
				System.out.println("class predicating error");
				e.printStackTrace();
				System.out.println(e.getMessage());
			}
		}
	}
	
	public void outClassifyResults(ArrayList<FileClass>list) throws Exception{
		PrintWriter resultStream; 
		int size = list.size();
		
		try
		{
			resultStream = new PrintWriter(new FileOutputStream(resultsFile));
		}
		catch(FileNotFoundException e)
		{
			System.out.println("Error opening the results.class.");
			return;
		}
		
		for(int i=0;i<size;i++){
			FileClass fc = list.get(i);
			resultStream.println(fc.file_id+","+fc.cl_genre);
		}
		
		resultStream.close();
	}
	
	public void classfyTestInstances(ArrayList<FileClass> list, WekaClassifier classifier) throws Exception{
		int size = list.size();
		int featuresSize = featureItems.size(); //general features number

		int err=0;
		for(int i=0;i<size;i++){
			SparseInstance sInstance = new SparseInstance(featuresSize);
			String result;
			FileClass fc = list.get(i);
			ArrayList<StemItem> al_si = fc.features;
			
			for(int j=0;j<featuresSize;j++)sInstance.setValue(j, 0);
			
			for(int j=0;j<al_si.size();j++){
				StemItem si = al_si.get(j);
				int index = si.index;
				int freq = 1;  //or si.freq;
				sInstance.setValue(index, freq);
			}
			result = classifier.classifyInstance(sInstance);
			fc.cl_genre = result;
			
			if(evalMode)if(!fc.genre.equals(fc.cl_genre))err++;
			
		}
		if(evalMode)System.out.println("There are "+err+" instances are classified wrong!");
	}
	
	public void devFeature(){
		//input file list file
		inputClassFiles(devClass); /* read train/dev.class */
		// input the files itself and parse them into the stem list form
		String[] dir = devClass.split("\\.");
		inputFiles(devList, dir[0]);  /* read files in *.class list */

		featuringFiles(devList);
		
		ARFFCreating(devList,'d');
		
		if(evalMode)System.out.println("Developing file is created.");
		
	}
	
	public void startTrainning(){
		//input stop words
		inputStopWords(stopWordsFile);
		
		//input file list file
		inputClassFiles(trainClass); /* read train/dev.class */
		// input the files itself and parse them into the stem list form
		String[] dir = trainClass.split("\\.");
		inputFiles(trainList, dir[0]);  /* read files in *.class list */
		
		// count the stem occur frequency
		freqCount(trainList);
		
		// adjusting the class freq list with their difference to general freq
		liftFreq(AFreqList);
		liftFreq(BFreqList);
		liftFreq(CFreqList);
		liftFreq(DFreqList);
		liftFreq(EFreqList);
		liftFreq(FFreqList);
		liftFreq(GFreqList);
		liftFreq(HFreqList);
		
		// sorting the class freq list base on freq, and trim list to no more than 200items
		Collections.sort(AFreqList);
		Collections.sort(BFreqList);
		Collections.sort(CFreqList);
		Collections.sort(DFreqList);
		Collections.sort(EFreqList);
		Collections.sort(FFreqList);
		Collections.sort(GFreqList);
		Collections.sort(HFreqList);
		
		// remove the stem item which occurs in all class freq list
//		rmCommItems();

		System.out.println("featureWordsCreating");
		featuresCreating();
		
		featuringFiles(trainList);
		
		ARFFCreating(trainList,'t');
		if(evalMode)logging(trainList);
	}
	
	public void logging(ArrayList<FileClass> fileList){
		int size = fileList.size();
		Iterator<String> itr;
		
		outputStream.println("Feature words list:");
		itr = featureWords.iterator();
		while(itr.hasNext()){
			outputStream.print(itr.next()+" ,");
		}
		outputStream.println();
		
		for (int i=0; i<size; i++){
			FileClass fc = fileList.get(i);
			String file_id = "File Namw:"+fc.file_id + "    Class:" +fc.genre+" , Features: ";
			String features="";
			
			int fsize = fc.features.size();
			
			for(int j=0;j<fsize;j++){
				features = features+", "+fc.features.get(j).stem+ ":"+fc.features.get(j).freq+":"+fc.features.get(j).index;
			}
			outputStream.print(file_id);
			outputStream.println(features);
		} 
		
		outputStream.close();
	}

	public void ARFFCreating(ArrayList<FileClass> fileList,char stage){
		String realtion = "@relation";
		String attribute = "@attribute";
		String data = "@data";
		String dataType = "NUMERIC";
		String genType = "{A, B, C, D, E, F, G, H}";
		
		PrintWriter arffStream;
		try
		{
			if(stage == 't'){
				arffStream = new PrintWriter(new FileOutputStream(trainArff));
			}
			else if(stage=='d'){				
				arffStream = new PrintWriter(new FileOutputStream(devArff));
			}
			else throw new FileNotFoundException();
		}
		catch(FileNotFoundException e)
		{
			System.out.println("Error opening the arffStream.");
			return;
		}
		
		arffStream.println(realtion+" Train_Files_Feature");
		arffStream.println();
		
		for(int i=0; i<featureItems.size(); i++){
			String feature = featureItems.get(i).stem;
			arffStream.println(attribute +" "+feature+" "+ dataType);
		}
		if(evalMode){
			arffStream.println(attribute+" class "+genType);
		}
		else if(stage == 't'){
			arffStream.println(attribute+" class "+genType);
		}
			
		arffStream.println();
		arffStream.println(data);

		int size = fileList.size();
		for (int i=0; i<size; i++){
			FileClass fc = fileList.get(i);
			ArrayList<StemItem> fList=fc.features;
			int fsize = fList.size();
			
			String dataStr = "{";
			for(int j=0;j<fsize;j++)dataStr += fList.get(j).index+" "+fList.get(j).freq+", ";

			if(evalMode){
				arffStream.print(dataStr + featureItems.size()+" "+fc.genre+"}");
			}
			else if(stage == 't'){
				arffStream.print(dataStr + featureItems.size()+" "+fc.genre+"}");
			}
			else arffStream.print(dataStr + "}");
			arffStream.println();
		} 
		
		arffStream.close();
	}
	
/**
 * creating the features for each file base the general features list
 * 1:	traval every FileClass in the input file list
 * 2: 	traval every stem of that fileclass item
 * 3: 	if the stem is a item of the general feature, then it is a file feature
 */
	public void featuringFiles(ArrayList<FileClass> fileList){
		int size = fileList.size();
		
		for(int i=0;i<size;i++){
			FileClass fc = fileList.get(i);
			ArrayList<StemItem> stList = fc.stemList;  //stem list of this file
			int stSize = stList.size();  //file stem list size
			int len = featureItems.size(); //general features number

			for(int j=0;j<len;j++){
				//if the stem in the global features, add it to file features list
				for(int k=0;k<stSize;k++){
					StemItem stem = stList.get(k);
					if(featureItems.get(j).equals(stem)){
						stem.index = featureItems.get(j).index;
						stem.freq = 1;   //remove frequency info
						fc.features.add(stem); 
					}
				}
			}
		}
	}

/**
 * geneFeatureCreating
 * generating genere feature words set
 */
	public void geneFeatureCreating(String genere){
		ArrayList<StemItem> freqList = new ArrayList<StemItem>();
		int size = trainList.size();
		
		if(genere.equals("A"))freqList = AFreqList;
		else if(genere.equals("B"))freqList = BFreqList;
		else if(genere.equals("C"))freqList = CFreqList;
		else if(genere.equals("D"))freqList = DFreqList;
		else if(genere.equals("E"))freqList = EFreqList;
		else if(genere.equals("F"))freqList = FFreqList;
		else if(genere.equals("G"))freqList = GFreqList;
		else if(genere.equals("H"))freqList = HFreqList;
		
		for(int i=0;i<size;i++){
			
		}
	}
	
/**
 * 	creating the general features from 8 class stem freq list
 */
	public void featuresCreating(){
		int i,len;
		
		len = AFreqList.size();
		if(BFreqList.size()<len)len = BFreqList.size();
		if(CFreqList.size()<len)len = CFreqList.size();
		if(DFreqList.size()<len)len = DFreqList.size();
		if(EFreqList.size()<len)len = EFreqList.size();
		if(FFreqList.size()<len)len = FFreqList.size();
		if(GFreqList.size()<len)len = GFreqList.size();
		if(HFreqList.size()<len)len = HFreqList.size();
		if(len>featureLen)len=featureLen;  //just choose the 50 most frequent words as the features
		
		featureWords.clear();

		for(i=0;i<len;i++){
			if(!AFreqList.get(i).stem.equals("class"))featureWords.add(AFreqList.get(i).stem);
			if(!BFreqList.get(i).stem.equals("class"))featureWords.add(BFreqList.get(i).stem);
			if(!CFreqList.get(i).stem.equals("class"))featureWords.add(CFreqList.get(i).stem);
			if(!DFreqList.get(i).stem.equals("class"))featureWords.add(DFreqList.get(i).stem);
			if(!EFreqList.get(i).stem.equals("class"))featureWords.add(EFreqList.get(i).stem);
			if(!FFreqList.get(i).stem.equals("class"))featureWords.add(FFreqList.get(i).stem);
			if(!GFreqList.get(i).stem.equals("class"))featureWords.add(GFreqList.get(i).stem);
			if(!HFreqList.get(i).stem.equals("class"))featureWords.add(HFreqList.get(i).stem);
		}
		
		Iterator<String> it = featureWords.iterator();
		
		featureItems.clear();
		i=0;
		while(it.hasNext()){
			String word = it.next();
			StemItem item = new StemItem(word);
			item.index = i;
			featureItems.add(item);
			i++;
		}
	}

/**
 * liftFreq
 * @param freqList
 * coefFreq adjust the stem freq in the freq list try to strength occur difference of a 
 * stem in different class
 * 1: it calculates the stem coef with the freq(Class)/freq(Gen)/8
 * 2: the new freq = old freq*coef**2
 * 3: remove all element which freq<1
 */
	public void liftFreq(ArrayList<StemItem> freqList){
		for(int i=0;i<freqList.size();i++){
			
			String item = freqList.get(i).stem;
			int freq = freqList.get(i).freq;
			
			for(int j=0;j<itemFreqList.size();j++){
				String target = itemFreqList.get(j).stem;
				
				if(target.equals(item)){
					double coef;
					int otherFreq = itemFreqList.get(j).freq - freq;
					if(otherFreq>0)coef = (double)freq/(double)(otherFreq)*7; 
					else coef = 100;
					freqList.get(i).coef = coef;
					freqList.get(i).freq = new Double(Math.pow(coef,1.3)*freq).intValue();
				}
			}
		}
	}
	
/**
 * freqCount
 * @param fileList
 * freqCount traval all the fileclass, and retrieving their stem freq,
 * then merge these stem and freq into the general freq list and 
 * 8 clsss freq stem lists respectively
 */
	public void freqCount(ArrayList<FileClass> fileList){
		System.out.println("freqCount");
		
		// traval every fileClass item 
		for (int i=0; i<fileList.size(); i++){
			FileClass fc = fileList.get(i);

			ArrayList<StemItem> stemList = fc.stemList; //retrieve stem list of the fileclass item
			String gen = fc.genre.toUpperCase();  // genre of the file
			
			// traval every stem item in the file class
			for(int j=0;j<stemList.size();j++){
				String stem = stemList.get(j).stem;  //stem string
				int freq = stemList.get(j).freq;  // frequency
				
				checkFreqList(itemFreqList,stem,freq);  //count into general freq list
				if(gen.equals("A"))checkFreqList(AFreqList,stem,freq); //into class 'A' freq list
				if(gen.equals("B"))checkFreqList(BFreqList,stem,freq); // B
				if(gen.equals("C"))checkFreqList(CFreqList,stem,freq); // C
				if(gen.equals("D"))checkFreqList(DFreqList,stem,freq);
				if(gen.equals("E"))checkFreqList(EFreqList,stem,freq);
				if(gen.equals("F"))checkFreqList(FFreqList,stem,freq);
				if(gen.equals("G"))checkFreqList(GFreqList,stem,freq);
				if(gen.equals("H"))checkFreqList(HFreqList,stem,freq);
			}
		}
	}
	
/**
 * checkFreqList
 * @param freqList: target stem freq list
 * @param item: stem string
 * @param freq: stem freq
 * Description:
 * checkFreqList insert the item/freq pair into the target stem freq list
 * firstly, it check whether the stem is already existing in the list
 * if existing, it add the input freq into the targwet list item
 * other wise, creating a new StemItem with input params and input it into list
 */
	public void checkFreqList(ArrayList<StemItem> freqList, String item, int freq){
		boolean newItem = true;
		
		//traval target list
		for(int k=0;k<freqList.size();k++){
			if(freqList.get(k).stem.equals(item)){  //if the item existing
				freqList.get(k).freq +=  freq;  //add the freq into target
				newItem = false;
				break;
			}
		}
		
		// otherwise, creating a new item
		if(newItem){
			StemItem si = new StemItem();
			si.stem = item;
			si.freq = freq;
			freqList.add(si);
		}
	}
	
/**
 *  remove the stem item which occurs in all the class freq list
 */
	public void rmCommItems(){
		System.out.println("Remove Common Items");
		
		ArrayList<String>  commStem = new ArrayList<String>();

		int len = AFreqList.size();
		for (int i=0; i<len; i++){
			String stem = AFreqList.get(i).stem;
			
			if(containItem(BFreqList,stem)&&containItem(CFreqList,stem)&&containItem(DFreqList,stem)
					&&containItem(EFreqList,stem)&&containItem(FFreqList,stem)&&containItem(GFreqList,stem)&&
					containItem(GFreqList,stem))commStem.add(stem);
		}
		
		String commstr="";
		for(int i=0;i<commStem.size();i++)commstr = commstr+commStem.get(i)+" ,";
		System.out.println(commstr);
		
		for(int i=0;i<commStem.size();i++){
			String item = commStem.get(i);

			rmItem(AFreqList,item);
			rmItem(BFreqList,item);
			rmItem(CFreqList,item);
			rmItem(DFreqList,item);
			rmItem(EFreqList,item);
			rmItem(FFreqList,item);
			rmItem(GFreqList,item);
			rmItem(HFreqList,item);
		}
	}
	
	public boolean containItem(ArrayList<StemItem>list, String item){
		int size = list.size();
		
		for (int i=0;i<size;i++){
			String stemStr = list.get(i).stem;
			if(stemStr.equals(item))return true;
		}
		return false;
	}
	
	public void rmItem(ArrayList<StemItem>list, String item){
		int len = list.size();
		for(int i=0;i<len;i++){
			if(list.get(i).stem.equals(item)){
				list.remove(i);
				break;
			}
		}
	}

/**
 * inputFiles
 * @param fileList: the file name list 
 * @param dir: the directory
 * 
 * 1st: inputFiles read the file from the input file list
 * 2nd: storing the file into the FileClass item
 * 3rd: stemming the input file text with fileClass' stemming method
 * 4th: normalizing the stem item frequency with fc.normFreq
 */
	public void inputFiles(ArrayList<FileClass> fileList,String dir){
		for (int i=0; i<fileList.size();i++){
			FileClass fc = fileList.get(i);
			String file_path = dir+"/"+fc.file_id;
			
			System.out.println("Reading file path:" + file_path);
			
			File textFile = new File(file_path);
			StringBuilder sb = new StringBuilder();
			String space = " ";
			
			if(textFile.exists()){
				try{
					Scanner input = new Scanner(new FileInputStream(textFile));   //creating the Scanner object

					while(input.hasNext()){
						String line = input.nextLine(); //read a line from text file
						
						sb = sb.append(line);
						sb = sb.append(space);
						}
					}
				catch(FileNotFoundException e){
					System.out.println("File name wrong: please check the file name and restarting");
					System.exit(0);
				}
				String text = sb.toString();
				int len = text.length();
				
				//remove copyright info
				int s_index = 500;
				int e_index = len-18000;
				text = text.substring(s_index, e_index);
				len = e_index-s_index;
				
				fc.text = text;
				fc.length = len;
				if(evalMode)System.out.println("file length:" + fc.length);
				fc.stemming();   /* change to stem list */
				fc.normFreq();
			}
			else System.out.println("textFile not existing!!");
		}
	}

/**
 * inputClassFiles
 * @param files
 * inputClassFiles read the input train/dec.class file 
 * and parsing every item into a FileClass item in a 
 * FileClass array
 */
	public void inputClassFiles(String files){
		File classFile = new File(files);
		String[] fileSec;
		
		if(classFile.exists()){
			try{
				Scanner input = new Scanner(new FileInputStream(classFile));   //creating the Scanner object

				while(input.hasNext()){
					String line;
					line = input.nextLine(); //read a line from book file
					if(line.length()<1)continue;
					fileSec = line.split(",");
					
					FileClass fc = new FileClass();
					fc.file_id = fileSec[0].trim();
					fc.genre = fileSec[1].trim();
					
					if(files.equals(trainClass))trainList.add(fc);
					else if(files.equals(devClass))devList.add(fc);
					}
				}
			catch(FileNotFoundException e){
				System.out.println("File name wrong: please check the file name and restarting");
				System.exit(0);
			}
		}
		else System.out.println("classFile not existing!!");
	}
	
	/**
	 * Read the stop words list
	 */
	public void inputStopWords(String files){
		File classFile = new File(files);
		
		if(classFile.exists()){
			try{
				Scanner input = new Scanner(new FileInputStream(classFile));   //creating the Scanner object

				while(input.hasNext()){
					String word;
					word = input.nextLine(); //read a line from input file
					word = word.trim();
					
					if(word.length()>0)stopWordsList.add(word);
				}
			}
			catch(FileNotFoundException e){
				System.out.println("File name wrong: please check the file name and restarting");
				System.exit(0);
			}
		}
		else System.out.println("stopFile not existing!!");
	}
/**
 * FileClass is used to store a single file information. 
 * 
 *
 */
	class FileClass {
		String file_id;   //file name 
		String genre;     //file class, must be in 'A','B','C','D','E','F','G','H'
		String cl_genre;  //the classified genre
		String text;
		int length;       //file length
		boolean b_featured;
		ArrayList<StemItem> stemList;  //the stem list of file
		ArrayList<StemItem> features;
		
		FileClass(){
			stemList = new ArrayList<StemItem>();
			features = new ArrayList<StemItem>();
			b_featured = false;
		}
		/**
		 *  stemming is transform the file into a list of stem.
		 *  1st step: change the file into the single word list
		 *  2nd: remove the words in stop word list
		 *  3rd: stemming the remain words
		 *  4th: count the remain stem frequency and store them into the atrrayList
		 */
		public void stemming(){
			String wordPattern = "\\b([A-Za-z]+)";  //word pattern
			Pattern pattern = Pattern.compile(wordPattern);
	        Matcher m = pattern.matcher(text);
	        
			if(evalMode)System.out.println("stemming");
			
			while(m.find()) {
				String stem = m.group().trim().toLowerCase();
				
				if(stopWordsList.contains(stem))continue;
			
				int len = stem.length();

				// stemming
				stemmer.add(stem.toCharArray(), len);
				stemmer.stem();
				stem = stemmer.toString();
				
				boolean newItem = true;
					
				//count the frequency
				for(int j=0;j<this.stemList.size();j++){
					StemItem si= this.stemList.get(j);
					if(si.stem.equals(stem)){
						si.freq = si.freq+1;
						newItem = false;
						break;
					}
				}
					
				if(newItem){
					StemItem si = new StemItem();
					si.stem = stem;
					si.freq = 1;
					this.stemList.add(si);
				}
			}
				text = "";
		}
		/**
		 * normFreq is try to normalise the stem frequency of different files into
		 * the unitify form
		 */
		public void normFreq(){
			if(evalMode)System.out.println("normFreq");
			
			ArrayList<StemItem> tmpList = new ArrayList<StemItem>();
			
			int len = stemList.size();
			for(int i = 0; i<len; i++){
				// the normFreq is the normalized stem occur frequency in the file
				double f = (double)(stemList.get(i).freq*100000)/(double)(length);
				int normFreq = new Double(f).intValue();
				
				if(normFreq > freqTh){  //freq must bigger than threshold
					StemItem si = new StemItem();
					si.freq = normFreq;
					si.stem = new String(stemList.get(i).stem);
						
					tmpList.add(si);
				}
			}
			this.stemList = tmpList;
		}
	}

	/**
	 * StemItem class is used to store a item, it has the stem and its frequency
	 *
	 */
	class StemItem implements Comparable<StemItem> {
		public String stem;
		public int freq;
		public int index;
		public double coef; //gene Freq/total Freq
		
		StemItem(){
			stem ="";
			freq = 1;
			coef = 1;
			index=0;
		}
		
		StemItem(String item){
			this.stem = item;
			this.freq = 1;
			this.coef = 1.0;
			this.index=0;
		}

		StemItem(String item,int freq){
			this.stem = item;
			this.freq = freq;
			this.coef = 1.0;
			this.index = 0;
		}

		StemItem(String item,int freq, double coef){
			this.stem = item;
			this.freq = freq;
			this.coef = coef;
			this.index = 0;
		}
		
		public boolean equals(StemItem otherItem){
			if ((this.stem.equals(otherItem.stem)))return true;
			return false;
		}
		
		public int compareTo(StemItem other){
			if(this.freq<other.freq)return 1;
			if (this.freq==other.freq)return 0;
			return -1;
		}
	}
}
