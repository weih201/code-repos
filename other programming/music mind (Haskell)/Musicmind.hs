-- vim: ts=4 sw=4 expandtab syntax=haskell

--	File     : Musicmind.hs
--	Author   : Wei Han (weih 523979)
--	Date     : Sat Sep. 3
--	Purpose  : The program for Declarative Programming COMP 90048 Project 1
--	
--	Description: This is the Game of Musicmind Soultion Seeking Source Code.
--      The export functions in this midule are:
--      1) initialGuess::([String],GameState)
--	   which output the init guess and initial GameState list
--      2) nextGuess::([String],GameState)->(Int,Int,Int)->([String],GameState)
--        which input the previous guess,GameState list and the feedback 
--	  and output the next guess and GameState list
--     
--    The most import data type in this program is the GameState type
--    GameState is a list type of the Chord type
--    A GameState type list variable contains all the remain possible Chord
--    The initial GameState variable: gamestate have all the 1330 possible Chord
--    Then in every nextGuess call, nextGuess will filter out all unsuitable 
--    Chord from that list untill reach the Target    
------------------------------------------------------------------------------            

module Musicmind (initialGuess, nextGuess, GameState) where

import Data.List

-----------------------------------------------------------------------------
--  Below are the data structure and data varibale used in this program:

--  The list pitch includes all the possible of pitch composition
pitch = ["A1","A2","A3","B1","B2","B3","C1","C2","C3","D1","D2","D3",
                       "E1","E2","E3","F1","F2","F3","G1","G2","G3"]

-- the Chord structure consists of three pitch which is the String type
data Chord = Chord String String String
			  deriving(Eq,Ord)

-- Overloading the Show function of the Chord to output the display 
-- as the deisre form to convient debugging
showChord :: Chord->String
showChord (Chord p1 p2 p3)= "("++(show p1) ++ (show p2) ++ (show p3)++")"
instance Show Chord where show = showChord

-- chordToString function change a Chord into the [String] form 
-- to meet the requirments of Musicmindtest.hs
chordToString :: Chord->[String]
chordToString (Chord p1 p2 p3)= [p1,p2,p3]

-- GameState type contains the system state info			  
type GameState = [Chord]

-- gamestate is an variable of the GameState type 
-- which store all the possible Chord for the system
gamestate:: GameState	
-- Compose the system Chord list, 
-- the possbile pitch can only come from the list: "pitch"
-- For no repetition pitch can occur in one Chord, so have: p1<p2,p2<p3
gamestate = [(Chord p1 p2 p3) | p1<-pitch, p2<-pitch,p3<-pitch,p1<p2,p2<p3] 


----------------------------------------------------------------------------
-- Below are two export functiones defined in this module:

-- The initialGuess function give the init guess
-- It output the initial guess and the gamestate list
initialGuess::([String],GameState)
initialGuess = (initguess,gamestate)  -- return init guess and gamestate list
-- initial guess can be any valid Chord, 
-- a better guess can reduce the guess number
          where initguess = ["A1","B2","E2"]  

-- The nextGuss function is the recursive function to seek the target Chord
-- It input the previous guess, 
nextGuess::([String],GameState)->(Int,Int,Int)->([String],GameState)
nextGuess (lastguess, gameState)  (right,rightNote,rightOctave) =  
	((chordToString (head stateFilterOctave)),stateFilterOctave)
	       
	   -- filter out chord with wrong pitch number from input state
    where  stateFilterPitch = filter (pitchFilter lastguess right) 
	                                  gameState 
	   --filter out chord with wrong notember
           stateFilterNote = filter (noteFilter lastguess rightNote) 
		                             stateFilterPitch 
           --filter out chord with wrong octave number
           stateFilterOctave = filter (octaveFilter lastguess rightOctave)
                          		     stateFilterNote


---------------------------------------------------------------------------									 
--  Below are the helper functiones used in this module:

-- pitchFilter: check a Chord with the guess to see whether 
-- the correct pitch number same as the input response number 
pitchFilter :: [String]->Int->Chord->Bool
pitchFilter guess right targetChord = (right==pitchMatch)
	-- change the Chord into the [String] form
     where target = chordToString targetChord    
	-- calculate the same pitch number
           pitchMatch = length $ intersect guess target  

-- noteFilter: check a Chord with the guess to see whether 
-- the correct note number same as the input response number 
noteFilter :: [String]->Int->Chord->Bool
noteFilter guess right targetChord = (right == noteMatch)
	-- change the target Chord into the [String] form
    where target     = chordToString targetChord  
          pitchMatch = length (intersect guess target)
          num        = length guess
        -- calculate the correct number
          noteMatch  = num - (length $ deleteFirstsBy (eqNth 0) guess target)
 		                      - pitchMatch 
			
-- octaveFilter: check a Chord with the guess to see 
-- whether the correct octave number same as the input response number 
octaveFilter :: [String]->Int-> Chord ->Bool
octaveFilter guess right targetChord = (right == octaveMatch)
	-- change the target Chord into the [String] form
    where target = chordToString targetChord     
          right' = length $ intersect guess target
          num = length guess
        -- calculate the correct number
          octaveMatch =num-(length $ deleteFirstsBy (eqNth 1) guess target)
                		  - right'
						  
-- | eqNth n l1 l2 returns True iff element n of l1 is equal to 
--   element n of l2.  This function get from: Musicmindtest.hs
eqNth :: Eq a => Int -> [a] -> [a] -> Bool
eqNth n l1 l2 = (l1 !! n) == (l2 !! n)

-------------------  END of File: Musicmind.hs  ---------------------------
