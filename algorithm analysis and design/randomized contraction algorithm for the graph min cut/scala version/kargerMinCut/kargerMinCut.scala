/**
 * 
 */
package kargerMinCut

/**
 * @author hwei
 *
 */
import scala.io.Source

object kargerMinCut {

    val test1 = List(List(1, 2, 3, 4, 5), List(2, 3, 4, 1), List(3, 4, 1, 2), List(4, 1, 2, 3, 8),
             List(5, 1, 6, 7 ,8), List(6, 7, 8 ,5), List(7, 8, 5, 6), List(8 ,4, 6, 5, 7))  // exp 2
             
    val test2 = List(List(1, 19, 15, 36, 23, 18, 39 ), List(2, 36, 23, 4, 18, 26, 9), List(3, 35, 6, 16, 11), 
        List(4, 23, 2, 18, 24), List(5, 14, 8, 29, 21), List(6, 34, 35, 3, 16), List(7, 30, 33, 38, 28), 
        List(8, 12, 14, 5, 29, 31), List(9, 39, 13, 20, 10, 17, 2),List(10, 9, 20, 12, 14, 29),
        List(11, 3, 16, 30, 33, 26), List(12, 20, 10, 14, 8), List(13, 24, 39, 9, 20),List(14, 10, 12, 8, 5),
        List(15, 26, 19, 1, 36), List(16, 6, 3, 11, 30, 17, 35, 32),List(17, 38, 28, 32, 40, 9, 16),
        List(18, 2, 4, 24, 39, 1),List(19, 27, 26, 15, 1),List(20, 13, 9, 10, 12),
        List(21, 5, 29, 25, 37), List(22, 32, 40, 34, 35), List(23, 1, 36, 2, 4),
        List(24, 4, 18, 39, 13), List(25, 29, 21, 37, 31), List(26, 31, 27, 19, 15, 11, 2),
        List(27, 37, 31, 26, 19, 29), List(28, 7, 38, 17, 32), List(29, 8, 5, 21, 25, 10, 27),
        List(30, 16, 11, 33, 7, 37), List(31, 25, 37, 27, 26, 8), List(32, 28, 17, 40, 22, 16),
        List(33, 11, 30, 7, 38), List(34, 40, 22, 35, 6), List(35, 22, 34, 6, 3, 16),
        List(36, 15, 1, 23, 2), List(37, 21, 25, 31, 27, 30), List(38, 33, 7, 28, 17, 40),
        List(39, 18, 24, 13, 9, 1), List(40, 17, 32, 22, 34, 38 ))  // expect: 3

  def main(args: Array[String]): Unit = {
	// reading data file and converting it to List[Array[String]]  form
     val verticeStrList = Source.fromFile("./data/kargerMinCut.txt" ).getLines.map(_.toString()).toList.map(_.split("[\t\n]"))
	// converting List[Array[String]] form to List[List[Int]] form
     val verticeList = verticeStrList.map{(v:Array[String])=>v.map(_.toInt).toList}
      
//     for (vertices <- verticeList;vertice<-vertices) println(vertice)
     println("Vertices number =: "+verticeList.length)
     
     val (minCut,minEdges) = kargerMinCut(verticeList)
     
     println("The minumum cut number is : "+minCut)
     println("The edges cross the cut are:")
     for ((u,v)<-minEdges) println("( "+u+" , "+v+" )")
  }
  
	def kargerMinCut(vertices:List[List[Int]]): (Int, List[(Int,Int)]) = {
	    val edges = vertToEdges(vertices,List[(Int,Int)]())
	    
	    println("Initial length of vertices: "+vertices.size)
	    println("Initial length of edges: "+edges.length)
	    
	    val rmEdges = removeDuplication(edges,List[(Int,Int)]())
	    
	    var minCut = edges.length
	    var minCutEdges = List[(Int,Int)]()
	    var i=0
	    while(i<100){
	        val (cut,cutEdges) = contraction(edges)
	        if (cut<minCut){
	            minCut = cut
	            minCutEdges = cutEdges
	        }
	        i+=1
	    }
	    return (minCut,minCutEdges)
	}
	
	def contraction(edges:List[(Int,Int)]):(Int,List[(Int,Int)]) = {
	    var vertices = Set[Int]()
	    for ((u,v) <- edges){
	        vertices += u
	        vertices += v
	    }
	 
	    if (vertices.size >2) {
	    	val r = scala.util.Random
	        val (u,v) = edges(r.nextInt(edges.length))
	        var newEdges = List[(Int,Int)]()   
	        
	        var i=0
	        while(i<edges.length)
	        {
		        val  (ui,vi) = edges(i)
		        
		        if (ui == v)
		                newEdges = (u,vi)::newEdges
		        else if(vi==v)
		                newEdges = (ui,u)::newEdges
		        else
		                newEdges = (ui,vi)::newEdges
		        i +=1
		    }
	    	val rmNewEdges = removeSelfLoop(newEdges,List[(Int,Int)]())
	    	
	        contraction(rmNewEdges) 
	    }
	   else       return (edges.length,edges)
	}
	   
	def vertToEdges(vertices:List[List[(Int)]],edges:List[(Int,Int)]):List[(Int,Int)] = 
	   vertices match {
		  case Nil => removeDuplication(edges,List[(Int,Int)]())
		  case vt::vts => {
		    val snode = List.fill(vt.tail.length)(vt.head)
		    val v_edges = snode zip vt.tail
		    removeDuplication(vertToEdges(vts,v_edges:::edges),List[(Int,Int)]())
		  }
	}
	
	def removeDuplication(edges:List[(Int,Int)],uniedges:List[(Int,Int)]):List[(Int,Int)] = edges match {
	  case Nil => uniedges
	  case (p,v)::ex =>{
	    if (uniedges.contains((p,v))||uniedges.contains((v,p))) {
	      removeDuplication(ex,uniedges)
	    }
	    else {
	      removeDuplication(ex,(p,v)::uniedges)
	    }
	  } 
	}

	def removeSelfLoop(edges:List[(Int,Int)],uniedges:List[(Int,Int)]):List[(Int,Int)] = edges match {
	  case Nil => uniedges
	  case (p,v)::ex =>{
	    if (p==v) {
	      removeSelfLoop(ex,uniedges)
	    }
	    else {
	      removeSelfLoop(ex,(p,v)::uniedges)
	    }
	  } 
	}
	
}