package recfun
import common._

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
   * Exercise 1
   */
  def pascal(c: Int, r: Int): Int = 
  {
    if(c<0 || c>r)0
    else if(r==0)1
    else pascal(c-1,r-1)+pascal(c,r-1)
  }

  /**
   * Exercise 2
   */
  def balance(chars: List[Char]): Boolean = 
  {
    
 	    chars match{
	    case List() => true
	    case ch::chx => if(ch==')')false
	    		else if(ch=='(') bal(chx) == -1
	    		else bal(chx)==0

/*	    case ch::chx => if(ch==')')false
	    		else if(ch=='('){
	    		  if(bal(chx) == -1)true
	    		  else false
	    		}
	    		else if(bal(chx)==0)true
	    		else false
*/	 
	    }
 }
  
 	def bal(chs:List[Char]):Int =  //0:balance; >0: extra number of '('; <0: extra number of ')'
	{
	  chs match{
	    case List()=>0
	    case ch::chx => if(ch==')')bal(chx)-1
	            else if(ch=='('){
	              if(bal(chx)==0)100
	              else bal(chx)+1
	            }
	            else bal(chx)
	  }
	}


  /**
   * Exercise 3
   */
  def countChange(money: Int, coins: List[Int]): Int = {
    
    if(money<0)0
    else if(money==0) 1
    else if(coins.isEmpty) 0
    else{
      coins match{
        case c::cx => countChange(money-c,coins)+countChange(money,cx)
      }
    }
  }
}
