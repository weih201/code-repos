package inversionCount

class mergeCount {
 
 /*   mcount implemented the inversion of number counting with the merge sort approach,
  *   but it used the global var variable to record the count
  */ 
	def mcount[T](less:(T,T)=>Boolean)(lst: List[T]): BigInt = {
		var count:BigInt =0                  
		def merge(left: List[T], right: List[T]): Stream[T] =
				(left, right) match {
				case (Nil, _) => right.toStream
				case (_, Nil) => left.toStream
				case (x :: xs, y :: ys) =>
					if (less(x,y)) Stream.cons(x,merge(xs, right))
					else {
					  count= count + left.length
					  Stream.cons(y, merge(left, ys))
					}
		}
		
		def mergecount(lst:List[T]):List[T] = {
			val n = lst.length/2
			if (n == 0) lst
			else {
				val (left, right) = lst splitAt n
				merge(mergecount(left), mergecount(right)).toList
			}
		}
	
		mergecount(lst)
		count
	}

/*
 *  mnvcount function improved the mcount function by removing the global variable  count 
 */	
	def mnvcount[T](less:(T,T)=>Boolean)(lst: List[T],count:Long): Long = {
	  
		def merge(left: List[T], right: List[T],count:Long):(List[T],Long) =
			(left, right) match {
			case (x :: xs, y :: ys) =>
				if (less(x, y)) {
				  val (xmerge,xcount) = merge(xs, right,count)
				  (x+:xmerge,xcount)
				}
				else {
				  val (ymerge,ycount) = merge(left, ys,count + left.length)
				  (y+:ymerge,ycount)
				}   
			case _ => (if (left.isEmpty) right else left, count)
		}
		
		def mergecount(lst:List[T],count:Long):(List[T],Long) = {
		  if (lst.length>1){
				val n = lst.length/2
				val (left, right) = lst splitAt n
				val (sortedLest, leftInversions) = mergecount(left,count)
				val (sortedRight,rightInversions) = mergecount(right,count)
				val (stream,inversions) = merge(sortedLest,sortedRight,leftInversions+rightInversions-count)
				(stream.toList,inversions)
		  }
		  else (lst,0)
		}
	
		mergecount(lst,count)._2
	}

}