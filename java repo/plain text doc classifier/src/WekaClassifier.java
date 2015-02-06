/*
 * Wei Han's New File
 *  Created on 21/05/2012
 */

import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.OptionHandler;
import weka.core.Utils;
import weka.classifiers.trees.J48;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.bayes.ComplementNaiveBayes;

import java.io.FileReader;
import java.io.BufferedReader;

public class WekaClassifier {
  /** the classifier used internally */
  private Classifier m_Classifier = null;
  
  /** the train file */
  private String m_trainFile = null;

  /** the dev file */
  private String m_devFile = null;

  /** the training instances */
  private Instances m_trainInstance = null;

  /** the testing instances */
  private Instances m_devInstance = null;

  /** for evaluating the classifier */
  private Evaluation m_Eval = null;

  public static enum Classification{
	  J48, NBC, CNB
  }
  
  public WekaClassifier() {
    super();
  }

  public WekaClassifier(String trainFile, String devFile) {
	    super();
	    this.m_trainFile = trainFile;
	    this.m_devFile = devFile;
  	}
 
  /**
   * create train, test  instances
   */
  public void creatInstance() throws Exception {
    m_trainInstance     = new Instances(
                        new BufferedReader(new FileReader(this.m_trainFile)));
    
    m_devInstance     = new Instances(
            new BufferedReader(new FileReader(this.m_devFile)));
    
    m_trainInstance.setClassIndex(m_trainInstance.numAttributes() - 1);
  }

  /**
   * sets the classifier to use
   */
  public void setClassifier(Classification classifier ) throws Exception {
    switch(classifier){
    case J48:
    	setJ48();
    	break;
    case NBC:
    	setNBC();
    	break;
    case CNB:
    	setCNB();
    	break;
    }
  }
  /**
   * set J48 decision tree
   */
  public void setJ48() throws Exception{
	  String[] options = new String[1];
	  options[0] = "-U";        // unpruned tree
	  m_Classifier = new J48(); 
	  System.out.println("J48 tree created");
//	  m_Classifier = Classifier.forName("J48", options);
  }

  /**
   * set naieve bayes classification
   */
  public void setNBC() throws Exception{
	  String[] options = new String[1];
	  options = null;        // use default
	  m_Classifier = new NaiveBayes(); 
//	  m_Classifier = Classifier.forName("NaiveBayes", options);
  }
  
  /**
   *  set complemental bayes classification
   */
  public void setCNB() throws Exception{
	  String[] options = new String[1];
	  options[0] = "-N";        //normalizing weight
	  m_Classifier = new ComplementNaiveBayes(); 
//	  m_Classifier = Classifier.forName("ComplementNaiveBayes", options);
  }

  /**
   * training and evaluating 
   */
  public void buildModel(boolean evalMode) throws Exception {
    // training
    m_Classifier.buildClassifier(m_trainInstance);
    
    if(evalMode){
        // evaluating
        m_devInstance.setClassIndex(m_trainInstance.numAttributes() - 1);
        m_Eval = new Evaluation(m_trainInstance);
        m_Eval.evaluateModel(m_Classifier, m_devInstance);
        System.out.println(m_Eval.toSummaryString("\nResults\n======\n", false));
    }
  }
  
  /*
   * predicating the class of data set in the devInstance 
   */
  public void classifyDataSet() throws Exception{
	  int size = m_devInstance.numInstances();
	  Instances testset = m_trainInstance.stringFreeStructure();

	  for(int i=0; i<size;i++){
		  // Make message into test instance.
		  Instance instance = m_trainInstance.instance(i); 
		  
		  instance.setDataset(testset);
		  // Get index of predicted class value.
		  double predicted = m_Classifier.classifyInstance(instance);
		  // Output class value.
		  System.out.println("The %dth books is classified as : " +
				  m_trainInstance.classAttribute().value((int)predicted));	
	  }
  }

  /*
   * predicating the class of a single Instance 
   * return the classify result
   */
  public String classifyInstance(Instance instance) throws Exception{
	  Instances testset = m_trainInstance.stringFreeStructure();

	  instance.setDataset(testset);
		  // Get index of predicted class value.
	  double predicted = m_Classifier.classifyInstance(instance);
		  // Output class value.
	  return (String)m_trainInstance.classAttribute().value((int)predicted);	
  }
  /**
   * outputs classifier data
   */
  public String toString() {
    StringBuffer        result;

    result = new StringBuffer();
    result.append("Weka - Classifer\n===========\n\n");

    result.append("Classifier...: " 
        + m_Classifier.getClass().getName() + " " 
        + Utils.joinOptions(m_Classifier.getOptions()) + "\n");
    result.append("Training file: " 
        + m_trainFile + "\n");
    result.append("\n");

    result.append(m_Classifier.toString() + "\n");
    result.append(m_Eval.toSummaryString() + "\n");
    
    try {
      result.append(m_Eval.toMatrixString() + "\n");
    }
    catch (Exception e) {
      e.printStackTrace();
    }
    
    try {
      result.append(m_Eval.toClassDetailsString() + "\n");
    }
    catch (Exception e) {
      e.printStackTrace();
    }
    
    return result.toString();
  }
}
