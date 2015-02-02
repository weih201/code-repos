package streams

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

import Bloxorz._

@RunWith(classOf[JUnitRunner])
class BloxorzSuite extends FunSuite {

  trait SolutionChecker extends GameDef with Solver with StringParserTerrain {
    /**
     * This method applies a list of moves `ls` to the block at position
     * `startPos`. This can be used to verify if a certain list of moves
     * is a valid solution, i.e. leads to the goal.
     */
    def solve(ls: List[Move]): Block =
      ls.foldLeft(startBlock) { case (block, move) => move match {
        case Left => block.left
        case Right => block.right
        case Up => block.up
        case Down => block.down
      }
    }
  }

  trait Level1 extends SolutionChecker {
      /* terrain for level 1*/

    val level =
    """ooo-------
      |oSoooo----
      |ooooooooo-
      |-ooooooooo
      |-----ooToo
      |------ooo-""".stripMargin

    val optsolution = List(Right, Right, Down, Right, Right, Right, Down)
  }

  test("terrain function level 1") {
    new Level1 {
      assert(terrain(Pos(0,0)), "0,0")
      assert(terrain(Pos(2,3)), "2,3")
      assert(!terrain(Pos(0,5)), "0,5")
      assert(!terrain(Pos(5,2)), "5,2")
      assert(!terrain(Pos(4,11)), "4,11")
      assert(!terrain(Pos(-1,1)), "-1,1")
    }
  }

  test("findChar level 1") {
    new Level1 {
      assert(startPos == Pos(1,1))
      assert(goal == Pos(4,7))
    }
  }

  test("Block same") {
    new Level1 {
      assert(Block(Pos(3,2), Pos(3,3)).equals(Block(Pos(3,2), Pos(3,3))))
    }
  }
  
  test("Neighours") {
    new Level1 {
      assert(Block(Pos(3,2), Pos(3,3)).neighbors.toSet === List((Block(Pos(2,2),Pos(2,3)),Up),(Block(Pos(3,1),Pos(3,1)),Left),
          (Block(Pos(3,4),Pos(3,4)),Right),(Block(Pos(4,2),Pos(4,3)),Down)).toSet)
    }
  }
  
  test("Legal Neighours") {
    new Level1 {
      assert(Block(Pos(3,2), Pos(3,3)).legalNeighbors.toSet === List((Block(Pos(2,2),Pos(2,3)),Up),(Block(Pos(3,1),Pos(3,1)),Left),
          (Block(Pos(3,4),Pos(3,4)),Right)).toSet)
    }
  }

  test("Legal Neighours 2") {
    new Level1 {
      assert(Block(Pos(3,4), Pos(3,4)).legalNeighbors.toSet === List((Block(Pos(3,2),Pos(3,3)),Left),(Block(Pos(1,4),Pos(2,4)),Up),
          (Block(Pos(3,5),Pos(3,6)),Right)).toSet)
    }
  }

  test(" startBlock") {
    new Level1 {
      assert(startBlock.equals(Block(Pos(1,1),Pos(1,1))))
    }
  }

  test(" startBlock isStanding") {
    new Level1 {
      assert(startBlock.isStanding)
    }
  }

  test("Neighours: startBlock") {
    new Level1 {
      assert(startBlock.neighbors.toSet === List((Block(Pos(1,2),Pos(1,3)),Right),(Block(Pos(2,1),Pos(3,1)),Down),
          (Block(Pos(1,-1),Pos(1,0)),Left),(Block(Pos(-1,1),Pos(0,1)),Up)).toSet)
    }
  }
  
  test("Legal Neighours: startBlock") {
    new Level1 {
      assert(startBlock.legalNeighbors.toSet === List((Block(Pos(1,2),Pos(1,3)),Right),(Block(Pos(2,1),Pos(3,1)),Down)).toSet)
    }
  }

  test("optimal solution for level 1") {
    new Level1 {
      assert(solve(solution) == Block(goal, goal))
    }
  }

  test("optimal solution length for level 1") {
    new Level1 {
      assert(solution.length == optsolution.length)
    }
  }
}
