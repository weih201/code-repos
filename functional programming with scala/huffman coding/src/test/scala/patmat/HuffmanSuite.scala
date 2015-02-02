package patmat

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

import patmat.Huffman._

@RunWith(classOf[JUnitRunner])
class HuffmanSuite extends FunSuite {
  trait TestTrees {
    val t1 = Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5)
    val t2 = Fork(Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5), Leaf('d',4), List('a','b','d'), 9)
  }

  test("weight of a larger tree") {
    new TestTrees {
      assert(weight(t1) === 5)
    }
  }

  test("chars of a larger tree") {
    new TestTrees {
      assert(chars(t2) === List('a','b','d'))
    }
  }

  test("string2chars(\"hello, world\")") {
    assert(string2Chars("hello, world") === List('h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd'))
  }
  
  test("times simple string") {
    assert(List(('a', 4)) === times(List('a','a','a','a')))
  }

  test("mixed string") {
	  assert(List(('a', 2), ('b', 1)) === times(List('a','b','a')))
  }

  test("times complex string") {
    assert(List(('a', 5), ('b', 5), ('c', 3), ('d', 2), ('e', 1)) === times(List('a','b','b','a','c','a','d','a','b','e','d','c','b','c','b','a')))
  }
  
  test("makeOrderedLeafList for some frequency table") {
    assert(makeOrderedLeafList(List(('t', 2), ('e', 1), ('x', 3))) === List(Leaf('e',1), Leaf('t',2), Leaf('x',3)))
  }

  test("singleton testing : true") {
    assert(singleton(List(Leaf('e',1))))
  }

  test("singleton testing: false") {
    assert(!singleton(List(Leaf('e',1), Leaf('t',2), Leaf('x',3))))
  }

  test("singleton testing: null false") {
    assert(!singleton(List()))
  }
  
  test("combine of some leaf list") {
    val leaflist = List(Leaf('e', 1), Leaf('t', 2), Leaf('x', 4))
    assert(combine(leaflist) === List(Fork(Leaf('e',1),Leaf('t',2),List('e', 't'),3), Leaf('x',4)))
  }

  test("until testing") {
    val leaflist = List(Leaf('e', 1), Leaf('t', 2), Leaf('x', 4))
    assert(until(singleton,combine)(leaflist) === List(Fork(Fork(Leaf('e',1),Leaf('t',2),List('e', 't'),3), Leaf('x',4),
        List('e','t','x'),7)))
  }

  test("encode a very short text ('ab')") {
    new TestTrees {
      assert(encode(t1)("ab".toList) === List(0,1))
    }
  }
  
  test("encode a little bit bigger text ('abbd')") {
    new TestTrees {
      assert(encode(t2)("abbd".toList) === List(0,0,0,1,0,1,1))
    }
  }

  test("decode and encode a very short text should be identity") {
    new TestTrees {
      assert(decode(t1, encode(t1)("ab".toList)) === "ab".toList)
    }
  }

  test("decode and encode a little bit bigger text ('abbd')") {
    new TestTrees {
      assert(decode(t2,encode(t2)("abbd".toList)) === "abbd".toList)
    }
  }

  test("decode and encode a  bigger text ('abbadbbbaad')") {
    new TestTrees {
      assert(decode(t2,encode(t2)("abbadbbbaad".toList)) === "abbadbbbaad".toList)
    }
  }

  test("decode and encode with quichencoding a  bigger text ('abbadbbbaad')") {
    new TestTrees {
      assert(decode(t2,quickEncode(t2)("abbadbbbaad".toList)) === "abbadbbbaad".toList)
    }
  }
}
