package funsets

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

/**
 * This class is a test suite for the methods in object FunSets. To run
 * the test suite, you can either:
 *  - run the "test" command in the SBT console
 *  - right-click the file in eclipse and chose "Run As" - "JUnit Test"
 */
@RunWith(classOf[JUnitRunner])
class FunSetSuite extends FunSuite {


  /**
   * Link to the scaladoc - very clear and detailed tutorial of FunSuite
   *
   * http://doc.scalatest.org/1.9.1/index.html#org.scalatest.FunSuite
   *
   * Operators
   *  - test
   *  - ignore
   *  - pending
   */

  /**
   * Tests are written using the "test" operator and the "assert" method.
   */
  test("string take") {
    val message = "hello, world"
    assert(message.take(5) == "hello")
  }

  /**
   * For ScalaTest tests, there exists a special equality operator "===" that
   * can be used inside "assert". If the assertion fails, the two values will
   * be printed in the error message. Otherwise, when using "==", the test
   * error message will only say "assertion failed", without showing the values.
   *
   * Try it out! Change the values so that the assertion fails, and look at the
   * error message.
   */
  test("adding ints") {
    assert(1 + 2 === 3)
  }

  
  import FunSets._

  test("contains is implemented") {
    assert(contains(x => true, 100))
  }
  
  /**
   * When writing tests, one would often like to re-use certain values for multiple
   * tests. For instance, we would like to create an Int-set and have multiple test
   * about it.
   * 
   * Instead of copy-pasting the code for creating the set into every test, we can
   * store it in the test class using a val:
   * 
   *   val s1 = singletonSet(1)
   * 
   * However, what happens if the method "singletonSet" has a bug and crashes? Then
   * the test methods are not even executed, because creating an instance of the
   * test class fails!
   * 
   * Therefore, we put the shared values into a separate trait (traits are like
   * abstract classes), and create an instance inside each test method.
   * 
   */

  trait TestSets {
    val s1 = singletonSet(1)
    val s2 = singletonSet(2)
    val s3 = singletonSet(3)
    val s4 = singletonSet(3)
    val s5 = singletonSet(999)
    val s6 = singletonSet(-1000)
  }

  /**
   * This test is currently disabled (by using "ignore") because the method
   * "singletonSet" is not yet implemented and the test would fail.
   * 
   * Once you finish your implementation of "singletonSet", exchange the
   * function "ignore" by "test".
   */
  test("singletonSet(1) contains 1") {
    
    /**
     * We create a new instance of the "TestSets" trait, this gives us access
     * to the values "s1" to "s3". 
     */
    new TestSets {
      /**
       * The string argument of "assert" is a message that is printed in case
       * the test fails. This helps identifying which assertion failed.
       */
      assert(contains(s1, 1), "Singleton")
    }
  }

  test("union contains all elements") {
    new TestSets {
      val s = union(s1, s2)
      assert(contains(s, 1), "Union 1")
      assert(contains(s, 2), "Union 2")
      assert(!contains(s, 3), "Union 3")
    }
  }

  test("interset contains all elements") {
    new TestSets {
      val s12 = union(s1, s2)
      val s123 = union(s12,s3)
      val s1234 = union(s123,s4)
      val s56 = union(s5,s6)
      val s123456 = union(s1234,s56)
      
      val s = intersect(s1234,s123456)
      
      assert(contains(s, 1), "Interset 1")
      assert(contains(s, 2), "Interset 2")
      assert(contains(s, 3), "Interset 3")
      assert(!contains(s, 999), "Interset 5")
      assert(!contains(s, -1000), "Interset 6")
    }
  }


  test("diff testing") {
    new TestSets {
      val s12 = union(s1, s2)
      val s123 = union(s12,s3)
      val s1234 = union(s123,s4)
      val s56 = union(s5,s6)
      val s123456 = union(s1234,s56)
      
      val s = diff(s123456,s1234)
      
      assert(!contains(s, 1), "diff 1")
      assert(!contains(s, 2), "diff 2")
      assert(!contains(s, 3), "diff 3")
      assert(contains(s, 999), "diff 5")
      assert(contains(s, -1000), "diff 6")
    }
  }


  test("filter testing") {
    new TestSets {
      val s12 = union(s1, s2)
      val s123 = union(s12,s3)
      val s1234 = union(s123,s4)
      val s56 = union(s5,s6)
      val s123456 = union(s1234,s56)
      
      val s = filter(s123456,(x:Int)=>x%2==0)
      
      assert(!contains(s, 1), "filter 1")
      assert(contains(s, 2), "filter 2")
      assert(!contains(s, 3), "filter 3")
      assert(!contains(s, 999), "filter 999")
      assert(contains(s, -1000), "filter -1000")
    }
  }

  test("forall testing") {
    new TestSets {
      val s12 = union(s1, s2)
      val s123 = union(s12,s3)
      val s1234 = union(s123,s4)
      val s56 = union(s5,s6)
      val s123456 = union(s1234,s56)
      val s26 = union(s2,s6)
      
      val b2 = forall(s26,(x:Int)=>x%2==0)
      val b1 = forall(s123456,(x:Int)=>x%2==0)
     
      assert(b2, "forall 2")
      assert(!b1, "forall 1")
   }
  }


  test("exists testing") {
    new TestSets {
      val s12 = union(s1, s2)
      val s123 = union(s12,s3)
      val s1234 = union(s123,s4)
      val s56 = union(s5,s6)
      val s123456 = union(s1234,s56)
      val s26 = union(s2,s6)
      val s135 = diff(s123456,s26)
      
      val b1 = exists(s1234,(x:Int)=>x%2==0)
      val b2 = exists(s135,(x:Int)=>x%2==0)
     
      assert(b1, "exists 1")
      assert(!b2, "exists 2")
    }
  }


  test("map testing") {
    new TestSets {
      val s12 = union(s1, s2)
      val s123 = union(s12,s3)
      val s1234 = union(s123,s4)
      val s56 = union(s5,s6)
      val s123456 = union(s1234,s56)
      
      val s = map(s123,(x:Int)=>x*2)
      
      assert(!contains(s, 1), "map 1")
      assert(contains(s, 2), "map 2")
      assert(!contains(s, 3), "map 3")
      assert(contains(s, 4), "map 4")
      assert(contains(s, 6), "map 6")
    }
  }
}


