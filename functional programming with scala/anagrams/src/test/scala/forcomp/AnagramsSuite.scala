package forcomp

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

import Anagrams._

@RunWith(classOf[JUnitRunner])
class AnagramsSuite extends FunSuite {

  test("wordOccurrences: abcd") {
    assert(wordOccurrences("abcd") === List(('a', 1), ('b', 1), ('c', 1), ('d', 1)))
  }

  test("wordOccurrences: Robert") {
    assert(wordOccurrences("Robert") === List(('b', 1), ('e', 1), ('o', 1), ('r', 2), ('t', 1)))
  }

  test("sentenceOccurrences: Nil") {
    assert(sentenceOccurrences(List()) === List())
  }

  test("sentenceOccurrences: abcd e") {
    assert(sentenceOccurrences(List("abcd", "e")) === List(('a', 1), ('b', 1), ('c', 1), ('d', 1), ('e', 1)))
  }

  test("sentenceOccurrences: abcd EDCS") {
    assert(sentenceOccurrences(List("abcd", "EDCS")) === List(('a', 1), ('b', 1), ('c', 2), ('d', 2), ('e', 1),('s',1)))
  }

  test("dictionaryByOccurrences.getOrElse: List()") {
    assert(dictionaryByOccurrences.getOrElse(List(),List('a')) === List('a'))
  }

  test("dictionaryByOccurrences.get: null") {
    assert(dictionaryByOccurrences.get(List()).map(_.toSet) === None)
  }
  
  test("dictionaryByOccurrences: aa") {
    assert(dictionaryByOccurrences.get(List(('a', 2))).map(_.toSet) === None)
  }

  test("dictionaryByOccurrences.get: eat") {
    assert(dictionaryByOccurrences.get(List(('a', 1), ('e', 1), ('t', 1))).map(_.toSet) === Some(Set("ate", "eat", "tea")))
  }

  test("word anagrams: eat") {
    assert(wordAnagrams("eat").toSet === Set("ate", "eat","tea"))
  }

  test("word anagrams: married") {
    assert(wordAnagrams("married").toSet === Set("married", "admirer"))
  }

  test("word anagrams: player") {
    assert(wordAnagrams("player").toSet === Set("parley", "pearly", "player", "replay"))
  }

  test("subtract: lard - r") {
    val lard = List(('a', 1), ('d', 1), ('l', 1), ('r', 1))
    val r = List(('r', 1))
    val lad = List(('a', 1), ('d', 1), ('l', 1))
    assert(subtract(lard, r) === lad)
  }

  test("subtract: more complex - r") {
    val lard = List(('a', 4), ('d', 2), ('l', 5), ('r', 7))
    val r = List(('r', 6),('d',2))
    val lad = List(('a', 4), ('l', 5),('r',1))
    assert(subtract(lard, r) === lad)
  }

  test("subtract: not enough - r") {
    val lard = List(('a', 4), ('d', 2))
    val r = List(('a', 6),('d',1),('e',3))
    val lad = List(('d',1))
    assert(subtract(lard, r) === lad)
  }

  test("combinations: []") {
    assert(combinations(Nil) === List(Nil))
  }

  test("combinations: elem") {
    val elem = List(('a', 3))
    val elemcomb = List(
      List(),
      List(('a', 1)),
      List(('a', 2)),
      List(('a', 3))
    )
    assert(combinations(elem).toSet === elemcomb.toSet)
  }
  
  test("combinations: abba") {
    val abba = List(('a', 2), ('b', 2))
    val abbacomb = List(
      List(),
      List(('a', 1)),
      List(('a', 2)),
      List(('b', 1)),
      List(('a', 1), ('b', 1)),
      List(('a', 2), ('b', 1)),
      List(('b', 2)),
      List(('a', 1), ('b', 2)),
      List(('a', 2), ('b', 2))
    )
    assert(combinations(abba).toSet === abbacomb.toSet)
  }

  test("combinations: abccba") {
    val abba = List(('a', 2), ('b', 2),('c',1))
    val abbacomb = List(
      List(),
      List(('a', 1)),
      List(('a', 2)),
      List(('b', 1)),
      List(('a', 1), ('b', 1)),
      List(('a', 2), ('b', 1)),
      List(('b', 2)),
      List(('a', 1), ('b', 2)),
      List(('a', 2), ('b', 2)),
      List(('c',1)),
      List(('a', 1),('c',1)),
      List(('a', 2),('c',1)),
      List(('b', 1),('c',1)),
      List(('a', 1), ('b', 1),('c',1)),
      List(('a', 2), ('b', 1),('c',1)),
      List(('b', 2),('c',1)),
      List(('a', 1), ('b', 2),('c',1)),
      List(('a', 2), ('b', 2),('c',1))
    )
    assert(combinations(abba).toSet === abbacomb.toSet)
  }

  test("sentence anagrams: []") {
    val sentence = List()
    assert(sentenceAnagrams(sentence) === List(Nil))
  }

  test("sentence anagrams: Linux rulez") {
    val sentence = List("Linux", "rulez")
    val anas = List(
      List("Rex", "Lin", "Zulu"),
      List("nil", "Zulu", "Rex"),
      List("Rex", "nil", "Zulu"),
      List("Zulu", "Rex", "Lin"),
      List("null", "Uzi", "Rex"),
      List("Rex", "Zulu", "Lin"),
      List("Uzi", "null", "Rex"),
      List("Rex", "null", "Uzi"),
      List("null", "Rex", "Uzi"),
      List("Lin", "Rex", "Zulu"),
      List("nil", "Rex", "Zulu"),
      List("Rex", "Uzi", "null"),
      List("Rex", "Zulu", "nil"),
      List("Zulu", "Rex", "nil"),
      List("Zulu", "Lin", "Rex"),
      List("Lin", "Zulu", "Rex"),
      List("Uzi", "Rex", "null"),
      List("Zulu", "nil", "Rex"),
      List("rulez", "Linux"),
      List("Linux", "rulez")
    )
    assert(sentenceAnagrams(sentence).toSet === anas.toSet)
  }  

}
