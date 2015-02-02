import java.io.Serializable;

/*
 * Wei Han's New File
 *  Created on 23/08/2011
 *  Wei Han 523979
 */

public class Result implements Serializable{
	int errorCode;  // errocode
					// 0: success
					// -1: not found
					// -2: invalid word
					// -3: connection lost
					// -4: other error
	String[] meanings;  //
}
