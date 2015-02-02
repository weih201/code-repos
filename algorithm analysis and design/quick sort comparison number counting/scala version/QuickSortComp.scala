package quicksort

import scala.io.Source

object QuickSortComp {

  def main(args: Array[String]): Unit = {

     val requiedList = Source.fromFile("./data/QuickSort.txt" ).getLines.map(_.toInt).toList
     val test1000 = Source.fromFile("./data/test/1000.txt" ).getLines.map(_.toInt).toList
      
     println("Test1000 list length =: "+test1000.length)
     println("Problem list length =: "+requiedList.length)
     
     val (lst,count) = quickSortComp(requiedList,"m")
     println("The result list is ordered: "+isOrdered(lst))
     println("Comparison number: "+count)
  }
  
  def quickSortComp(arr:List[Int],pv:String):(List[Int],Long) = {
    if (arr.length<=1) return (arr,0)
    else{
      arr match {
	  	case _ => {
	  	  val (left,x,right) = partition(arr,pv)
	  	  val (l_list,l_c) = quickSortComp(left,pv)
	  	  val (r_list,r_c) = quickSortComp(right,pv)
	  	  return ((l_list:+x) ++ r_list,l_c+r_c+arr.length-1)
	  	}
      }
    }
  }
  
  def partition(arr:List[Int],pv:String):(List[Int],Int,List[Int]) = {
    val l = choosePivot(arr,pv)
    val arr1 = swap(arr,0,l)
    
    arr1 match {
      case a::ax => ((ax filter (a >)) , a, (ax filter (a <)))
    }
  }
  
  def choosePivot(arr:List[Int],pv:String):Int = {
    if (pv.equals("f")) return 0
    else if(pv.equals("l"))return arr.length-1
    else {
      val m = arr((arr.length-1)/2)
      val a = arr(0)
      val b = arr(arr.length-1)
      val med = math.max(math.min(a,b), math.min(math.max(a,b),m))
      
      if(med == a)return 0
      else if (med ==b )return arr.length-1
      else return (arr.length-1)/2
    }
  }
  
  def swap(arr:List[Int],i:Int,j:Int):List[Int] = {
	  val elem = arr(i)
	  val list1 = arr.updated(i, arr(j)).updated(j, elem)
	  return list1
  }

  def isOrdered(l:List[Int]): Boolean = l match {
	  case Nil => true
	  case x :: Nil => true
	  case x :: xs => x <= xs.head && isOrdered(xs)
	}
}