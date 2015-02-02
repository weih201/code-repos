--  File     : Musicmind.hs
--  Author   : Wei Han (weih 523979)
--  Date     : Sat Sep. 3
--  Purpose  : The program for Declarative Programming COMP 90048 Project 1
--           : The Game of Musicmind Soultion Seeking Source Code

module Musicmind (initialGuess, nextGuess, GameState) where

import Data.List
--  The list pitch includes all the possible of pitch composition
pitch = ["A1","A2","A3","B1","B2","B3","C1","C2","C3","D1","D2","D3","E1","E2","E3","F1","F2","F3","G1","G2","G3"]

-- the Chord structure consists of three pitch which is the String type
data Chord = Chord String String String
			  deriving(Eq,Ord)
-- Overloading the Show function of the Chord to output the display as the deisre form to convient debugging
showChord :: Chord->String
showChord (Chord p1 p2 p3)= "("++(show p1) ++ (show p2) ++ (show p3)++")"
instance Show Chord where show = showChord

-- chordToString function change a Chord into the [String] form to meet the requirments of Musicmindtest.hs
chordToString :: Chord->[String]
chordToString (Chord p1 p2 p3)= [p1,p2,p3]

-- GameState type contains the system state info			  
type GameState = [Chord]
-- gamestate is an variable of the GameState type which possible Chord for the system
gamestate:: GameState	
-- Compose the system Chord list, the possbile pitch can only come from the list; pitch
-- For no repetition pitch can occur in one Chord, so have: p1<p2,p2<p3
gamestate = [(Chord p1 p2 p3) | p1<-pitch, p2<-pitch,p3<-pitch,p1<p2,p2<p3] 

-- pitchFilter: check a Chord with the guess to see whether the correct pitch number same as the input response number 
pitchFilter :: [String]->Int->Chord->Bool
pitchFilter guess right targetChord = (right==pitchMatch)
     where target = chordToString targetChord       -- change the Chord into the [String] form
           pitchMatch = length $ intersect guess target  -- calculate the same pitch number

-- noteFilter: check a Chord with the guess to see whether the correct note number same as the input response number 
noteFilter :: [String]->Int->Chord->Bool
noteFilter guess right targetChord = (right == noteMatch)
    where target     = chordToString targetChord  -- change the target Chord into the [String] form
          pitchMatch = length (intersect guess target)
          num        = length guess
          noteMatch  = num - (length $ deleteFirstsBy (eqNth 0) guess target) - pitchMatch -- calculate the correct number
			
-- octaveFilter: check a Chord with the guess to see whether the correct octave number same as the input response number 
octaveFilter :: [String]->Int-> Chord ->Bool
octaveFilter guess right targetChord = (right == octaveMatch)
    where target = chordToString targetChord     -- change the target Chord into the [String] form
          right' = length $ intersect guess target
          num = length guess
          octaveMatch = num - (length $ deleteFirstsBy (eqNth 1) guess target) - right'  -- calculate the correct number

-- | eqNth n l1 l2 returns True iff element n of l1 is equal to 
--   element n of l2.   Come from: Musicmindtest.hs
eqNth :: Eq a => Int -> [a] -> [a] -> Bool
eqNth n l1 l2 = (l1 !! n) == (l2 !! n)

initialGuess::([String],GameState)
initialGuess = (initguess,gamestate)      -- the system initial state is the list: gamestate
          where initguess = ["A1","B2","E2"]    -- initial guess can be any valid Chord

nextGuess::([String],GameState)->(Int,Int,Int)->([String],GameState)
nextGuess (lastguess, gameState)  (right,rightNote,rightOctave) =  ((chordToString (head stateFilterOctave)),stateFilterOctave)
    where  stateFilterPitch = filter (pitchFilter lastguess right) gameState  -- filter out chord with wrong pitch number from input state
           stateFilterNote = filter (noteFilter lastguess rightNote) stateFilterPitch --filter out chord with wrong notember
           stateFilterOctave = filter (octaveFilter lastguess rightOctave) stateFilterNote --filter out chord with wrong octave number
		   
--  Monard version nextGuess, can work on desktop, but cannot work on server, I don't know why
--nextGuess (lastguess, gamestate)  (right,rightNote,rightOctave) =  do
--	let stateFilterPitch = filter (pitchFilter lastguess right) gamestate
--	let stateFilterNote = filter (noteFilter lastguess rightNote) stateFilterPitch
--	let stateFilterOctave = filter (octaveFilter lastguess rightOctave) stateFilterNote
--	((chordToString (head stateFilterOctave)),stateFilterOctave)

--nextGuessList::([String],GameState)->(Int,Int,Int)-> Int
--nextGuessList (lastguess, gameState)  (right,rightNote,rightOctave) =  do
--	let stateFilterPitch = filter (pitchFilter lastguess right) gamestate
--	let stateFilterNote = filter (noteFilter lastguess rightNote) stateFilterPitch
--	let stateFilterOctave = filter (octaveFilter lastguess rightOctave) stateFilterNote
--	length stateFilterOctave
