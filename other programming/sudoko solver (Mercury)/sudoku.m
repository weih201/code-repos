%  	File  	: sudoku.m
%	Author 	: wei han (weih 523979)
%	Date	: Sun. Oct. 23, 2011
%
%	Purpose:
%	The sudoku.m file is intend to solve Sudoku puzzle of any rank with Mercury
%	. Due to the limition of the character display, the current version can 
%	solve up to 5th rank Sudoku puzzle.
% 
%	Description:
%	The Sudoku solving approaches in this file are based on three techniques:
%
%	The first one is called unique-candidate: In the Sudoku puzzle, every 
%	allowable value can only appear once in every country (each row, each 
%	column, or each nxn sub-squre). So if a value already appear in a country,
%	it cannot appear in unknown cell in that country. So the unique-candidate
%	technique is to fill the unknown cell a value set as all the possible value
%	Then filter this value set with all the known values in its possible 
%	countries. If after all these filtering, a known cell just leave one
%	value, then that set's value is known. Even the left values number is not 
%	one, its possible vlaues number also greatly reduced after unique-candidate.
%	The predicate entry for unique-candidate in this file is:
%
%	:- pred unique_candidate(list(list(int))::in,int::in,int::in,
%		list(list(int))::out) is semidet.
%
%	In the unique_candidate predicate, if it found the output puzzle list has
%	the more known cell than the input puzzle list, it will call itself again
%	untill cannot find any new cell value or the puzzle solution is reach.
%
%	If the unique_candidate is not reach to the puzzle solution, it will call
%	the second technique.
%
%	The second technique is called unique-position. It is something oppose to 
%	the unique-candidate technique. It is based on every position in one country
%	must have one unique value. So if a value cannot appear in all the other 
%	unknown position in that country. Then it must appear in the only left 
%	possible unkown cell in that country. The predicate for unique-position in
%	this file is:
%	
%	:- pred unique_pos(list(list(int))::in,int::in,int::in,
%			list(list(int))::out) is semidet.
%
%	The implementation of the unique_pos is more complcated than 
%	unique_candidate for it involve with other country.
%	
%	This program transformed it into a simpler equivalent form which can be solved
%	within one country. After the unique_candidate, every cell can only include 
%	its values set. So if a value appear in one cell's possible value set, but 
%	cannot appear in all the other cell's value set in the same country, this 
%	means this value's unique postion in that country is the cell's vlaues set
%	contain it. So that cell's value is known.
%
%	If the puzzle solution is reach, the unique_pos will exit. 
%	If the unique_pos can find any new cell value, it will call 
%	unique_candidate again.
%
%	If it cannot find any new cell vlaue, it will exit. The program will try
%	the last technique, which is "guess" the unfilled cell's value. 
%	The predicate is:
%
%	:- pred guess_solution(list(list(int))::in,int::in,int::in,
%			list(list(int))::out) is nondet.
%
%	The guess_solution is based on Mercury's back tracking feature. It start 
%	from the first unfilled cell, select a value from its psosible vlaue set,
%	then call unique_candidate(including unique_pos) pred to reduce the inpiut 
%	puzzle list. Then it check whether the reduced list is a valid list.
%
%	If it is a valid list, then check whether it is a Sudoku solution. If it
%	is a valid solution, it exit. Otherwise, it forword to the next unfilled 
%	cell. And repeat again. 
%
%	If list is not a valid list, the guess_solution will back track to the
%	next previous unfilled possible value and repeat above procedure untill
%	reach to solution.
%
%	Supplement Comment:
%	This program is based on the sudoku-starter.m framework and grouping.m 
%	module both written by Peter Schachte.
%	
%	The predicate get from sudoku-starter.m is comment on the front of the 
%	predicate defination. The predicates from grouping.m are:
%	:- pred group_list(int, int, int, list(E), list(list(E))).
%	:- pred ungroup_list(int, int, int, list(E), list(list(E))).
%
%	Thanks Peter for providing these help.
%
:- module sudoku.
:- interface.
:- import_module io.
:- pred main(io::di, io::uo) is cc_multi.	

:- implementation.
:- import_module list, char, int, require, set, bool.
:- import_module grouping.

%  This predicate is get from sudoku-starter.m written by Peter Schachte

%	The main predicate read the coomand line input, check whether it's 
%	in correct form, otherwise, give the hint info
main(!IO) :-
	io.command_line_arguments(Args, !IO),
	(   Args = [File]
	->  io.see(File, Result, !IO),
	    (   Result = ok,
		sudoku(!IO),
		io.seen(!IO)
	    ;   Result = error(_),
		io.write_string("Could not open puzzle file\n", !IO),
		set_exit_status(1, !IO)
	    )
	;   usage(!IO),
	    set_exit_status(1, !IO)
	).

:- pred usage(io::di, io::uo) is det.
%  Print out a usage message for this program.

%  This predicate is get from sudoku-starter.m written by Peter Schachte

usage(!IO) :-
	io.write_string("Usage:  sudoku filname\n", !IO),
	io.write_string(
"  where filname is the name of a file containing a sudoku puzzle\n", !IO),
	io.write_string(
"  written as a file of 4, 9, 16, or 25 lines, each with that same\n", !IO),
	io.write_string(
"  number of characters.  All characters on each line must be either\n", !IO),
	io.write_string(
"  a space (for squares to be solved for) or a digit (except 0) or a\n", !IO),
	io.write_string(
"  letter.  A solved puzzle is the same, except that all spaces have\n", !IO),
	io.write_string(
"  been filled in with letters and digits, and each digit or letter\n", !IO),
	io.write_string(
"  between 1 and the width of the puzzle (where 'a' is taken for 10,\n", !IO),
	io.write_string(
"  and so on) appears exactly once in each row, column, and box.\n", !IO).


:- pred sudoku(io::di, io::uo) is cc_multi.	
%  This predicate is get from sudoku-starter.m written by Peter Schachte

%  It read a puzzle from the current input stream, solve it, and print
%  out the result.
sudoku(!IO) :-
	load_puzzle(Puzzle, !IO),
	(   Puzzle = []
	->  io.write_string("Error reading puzzle\n", !IO),
	    set_exit_status(1, !IO)
	;   valid_sudoku_size(length(Puzzle), Size, Boxsize)
	->  
	  ( 
	    solve_sudoku(Puzzle, Size, Boxsize, PuzzleOut),
	    print_puzzle(PuzzleOut, Size, Boxsize, !IO)
	   )
	;  io.write_string("Invalid puzzle size\n", !IO),
	    set_exit_status(1, !IO)
	).

% 	My Sudoku puzzle solution entry predicate
%	It transform input puzzle list into a list(list()) form
%	Then call unique_candidate and guess_solution to solve it
:- pred solve_sudoku(list(int)::in, int::in, int::in, 
					list(int)::out) is cc_multi.  

solve_sudoku(Puzzle, Size, Boxsize, Solution) :-
	puzzle_list(Puzzle, Boxsize, Puzzlelist),
	
	unique_candidate(Puzzlelist,Size,Boxsize,Puzzlelist2),
	
	onelen(Puzzlelist2,0,OneLen),
	
	(
		OneLen >= list.length(Puzzle)
		->
		list_puzzle(Puzzlelist2,Solution)
		;
		(
			guess_solution(Puzzlelist2,Size,Boxsize,Puzzlelist3),
			list_puzzle(Puzzlelist3,Solution)
			;
			list_puzzle(Puzzlelist2,Solution)
		)
	)
	;  
	Solution = list.duplicate(Size,0).
	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 	Uniques Candidate Predicate entry
%	This predicate filter a unfilled cell's possible values with
%	the known value in its possible country 
%	If only one value left in that cell, the value known, then it call itself 
% 	other wise, ity call unique_pos predicate
:- pred unique_candidate(list(list(int))::in,int::in,int::in,
		list(list(int))::out) is semidet.

unique_candidate(InputList,Size,Boxsize,OutputList):-
	group_list(Size,1,1,InputList,Group1),
	groupFilter(Group1,Group2),
	ungroup_list(Size,1,1,Puzzlelist1,Group2),
	
	group_list(1,Size,Size,Puzzlelist1,Group3),
	groupFilter(Group3,Group4),
	ungroup_list(1,Size,Size,Puzzlelist2,Group4),
	
	group_list(Boxsize,Boxsize,Boxsize,Puzzlelist2,Group5),
	groupFilter(Group5,Group6),
	ungroup_list(Boxsize,Boxsize,Boxsize,Puzzlelist3,Group6),
	
	onelen(InputList,0,InputLen),
	onelen(Puzzlelist3,0,OutputLen),
	
	(
	OutputLen>InputLen
	->
		unique_candidate(Puzzlelist3,Size,Boxsize,OutputList)
	;
	(
		OutputLen >= list.length(InputList)
		->
		OutputList = Puzzlelist3
		;
		unique_pos(Puzzlelist3,Size,Boxsize,OutputList)
	)
	).
	
% 	Group List filter 
% 	Filter all the list in one group
:- 	pred groupFilter(list(list(list(int)))::in, 
		list(list(list(int)))::out) is semidet.
	
groupFilter(InputList, OutputList):-
	InputList=[]
	-> OutputList=[]
	;
	InputList = [InputHead|InputTail],
	OutputList = [OutputHead|OutputTail],
	listFilter(InputHead,OutputHead),
	groupFilter(InputTail,OutputTail).
	
% 	Filter the List with al its all known elements
%	
:- 	pred listFilter(list(list(int))::in,  
		list(list(int))::out) is semidet.
	
listFilter(InputList, OutputList):-
	filterHelper(InputList,InputList,[], OutputList).
	
% 	Filter Helper pred 1
% 	This predicate pick the single length element from list, then call
% 	filterTarget predicate to filter target list
:- pred filterHelper(list(list(int))::in, list(list(int))::in,
	list(list(int))::in, list(list(int))::out) is semidet.
	
filterHelper(InputList, TargetList,TargetHead, OutputList):-
	InputList = []
	-> list.append(TargetHead,TargetList,OutputList)
	;
	InputList = [InputHead|InputTail],
	TargetList = [LTgtHead|LTgtTail],
	(
	list.length(InputHead) = 1
	->
	(	
	 list.index0(InputHead,0,Element) ,
	 filterTarget(Element,LTgtTail, TgtListTail),
	 filterTarget(Element,TargetHead, TgtListHead),

   	 list.append(TgtListHead,[LTgtHead],TgtHead),
	 filterHelper(InputTail,TgtListTail,TgtHead, OutputList)
	)
	;
   	 list.append(TargetHead,[LTgtHead],TgtHead),
	 filterHelper(InputTail,LTgtTail,TgtHead, OutputList)
	).

% 	Filter Helper pred 2
%	This predicate filter target list with the input element
:- 	pred filterTarget(int::in, list(list(int))::in,
		list(list(int))::out) is semidet.
	
filterTarget(Elem,TargetList,OutputList):-
	TargetList = []
	-> OutputList = []
	;
	TargetList = [TargetHead|TargetTail],
	OutputList = [OutputHead|OutputTail],
	
	(
		HeadSet = set.set(TargetHead),
		OutputSet = set.delete(HeadSet,Elem),
		OutputHead = set.to_sorted_list(OutputSet),
			
		filterTarget(Elem,TargetTail,OutputTail)
	).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 	Uniques Position Pred
%	This predicate check all the possible value in a country to see if there
%	is any vlaues just appear once in that country. If there exist such vlaue,
%	that unfilled cell's value should be that unique value.

:- pred unique_pos(list(list(int))::in,int::in,int::in,
		list(list(int))::out) is semidet.

unique_pos(InputList,Size,Boxsize,OutputList):-
	group_list(Size,1,1,InputList,Group1),
	groupCheck(Group1,Group2),
	ungroup_list(Size,1,1,Puzzlelist1,Group2),
	
	group_list(1,Size,Size,Puzzlelist1,Group3),
	groupCheck(Group3,Group4),
	ungroup_list(1,Size,Size,Puzzlelist2,Group4),
	
	group_list(Boxsize,Boxsize,Boxsize,Puzzlelist2,Group5),
	groupCheck(Group5,Group6),
	ungroup_list(Boxsize,Boxsize,Boxsize,Puzzlelist3,Group6),
	
	onelen(InputList,0,InputLen),
	onelen(Puzzlelist3,0,OutputLen),
	
	(
	OutputLen>InputLen
	->
		unique_candidate(Puzzlelist3,Size,Boxsize,OutputList)
	;
	OutputList = Puzzlelist3
	).
	
% 	Check the unique position value in all the listes of a group
:- 	pred groupCheck(list(list(list(int)))::in, 
	list(list(list(int)))::out) is semidet.
	
groupCheck(InputList, OutputList):-
	InputList=[]
	-> OutputList=[]
	;
	InputList = [InputHead|InputTail],
	OutputList = [OutputHead|OutputTail],
	listCheck(InputHead,OutputHead),
	groupCheck(InputTail,OutputTail).
	
% 	Check the unique position value in a list
%	Recurresively call itself untill all unique position values
%	have found
:- pred listCheck(list(list(int))::in, list(list(int))::out) is semidet.
	
listCheck(InputList, OutputList):-
	TargetList = InputList,
	uniPosHelper(InputList,TargetList,OutputList).

% 	List uni-position check helper predicate
:- pred uniPosHelper(list(list(int))::in, list(list(int))::in, 
	list(list(int))::out) is semidet.
	
uniPosHelper(InputList, TargetList, OutputList):-
	InputList = []
	-> OutputList = []
	;
	InputList = [InputHead|InputTail],
	OutputList = [OutputHead|OutputTail],
	(
	list.length(InputHead) > 1
	->
	uniqueElement(InputHead, InputHead, TargetList, OutputHead)
	;
	OutputHead = InputHead
	),
	uniPosHelper(InputTail,TargetList,OutputTail).
	
% 	Element list checking
:- pred uniqueElement(list(int)::in, list(int)::in, list(list(int))::in,
		list(int)::out) is semidet.
	
uniqueElement(InputList,OriginalHead, TargetList, OutputList):-
	InputList = []
	-> OutputList = OriginalHead
	;
	InputList = [InputHead|InputTail],
    countElement(InputHead,TargetList,0,Num),
	(
	Num > 1
	-> 
	uniqueElement(InputTail,OriginalHead, TargetList, OutputList)
	;
	OutputList = [InputHead]
	).
	
% 	Count a value appear number in a list's possible set
:- 	pred countElement(int::in, list(list(int))::in, int::in, 
		int::out) is semidet.
	
countElement(Element, TargetList, PreNum, CountNum):-
	TargetList = []
	-> CountNum = PreNum
	;
	TargetList = [TargetHead|TargetTail],
	(
	list.member(Element,TargetHead)
	->
	countElement(Element,TargetTail,PreNum + 1,CountNum)
	;
	countElement(Element,TargetTail,PreNum,CountNum)
	).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% 	Guess Solution Entry Predicate
:- pred guess_solution(list(list(int))::in,int::in,int::in,
		list(list(int))::out) is nondet.

guess_solution(InputList,Size,Boxsize,OutputList) :-
	guess_helper(InputList,InputList,Size,Boxsize,OutputList).
	
% 	Guess Solution Helper Pred
%	It start from first unfilled cell, pick a value from that set with
%	list_element, then update puzzle with unique_candidate, then call 
%	validList to check whether updated list is valid.
%	If valid and solution is not reach, it call itself to repeat next loop;
%	If solution is reach, exit;
%	If list is not valid, it back track to previous entry point and 
%	pick another value and call itself and repeat loop
:- pred guess_helper(list(list(int))::in,list(list(int))::in,int::in,
	int::in,list(list(int))::out) is nondet.

guess_helper(CurList, OrigList, Size,Boxsize,OutputList):-
	CurList = []
	->
	unique_candidate(OrigList,Size,Boxsize,OutputList)
	;
	CurList = [CurHead|CurTail],
	(
	list.length(CurHead) = 1
	->
	guess_helper(CurTail, OrigList,Size,Boxsize,OutputList)
	;
	(
	list_element(CurHead,Element),
	(
	updatelist(OrigList, [Element], [], NewList),
	unique_candidate(NewList,Size,Boxsize,NewList2),

	validList(NewList2),	
	(
		onelen(NewList2,0,OneLen),
		OneLen = list.length(OrigList)
		->
		OutputList = NewList2
		;
		guess_helper(CurTail, NewList, Size,Boxsize,OutputList)
	)
	)
	)
	).

%  	Check whether a puzzle list is vailid, 
%	A valid list in this scenario means the puzzle list don't have empty set
:- pred validList(list(list(int))::in) is semidet.

validList([]).
validList([H | T]) :-
    list.length(H)>0,
    validList(T).

% 	Update puzzle list with a guessed element value
:- pred updatelist(list(list(int))::in, list(int)::in,list(list(int))::in, 
	list(list(int))::out) is semidet.

updatelist(OrigList,Elem, CurList, NewList):-
	OrigList = []
	->	NewList = CurList
	;
	OrigList = [OrigHead|OrigTail],
	(
	list.length(OrigHead)=1
	->
	(
		TempList = list.append(CurList,[OrigHead]),
		updatelist(OrigTail, Elem, TempList,NewList)
	)
	;
	(
		TempList = list.append(CurList,[Elem]),
		list.append(TempList,OrigTail,TemList2),
		updatelist([], Elem, TemList2,NewList)
	)
	).
		
% pick a element from a list
:- pred list_element(list(int)::in, int::out) is nondet.

list_element([H | T], H).   
list_element([H | T], E) :-   
    list_element(T, E).
	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
%% Convert the puzzle into the list(list) form	
:-  pred puzzle_list(list(int)::in, int::in, 
		list(list(int))::out) is semidet.

puzzle_list(Puzzle, Boxsize, Puzzlelist):-
	Puzzle = []
	-> Puzzlelist =[]
	;
	(  Puzzle = [PuzzleHead|PuzzleTail],
	   Puzzlelist = [Puzzlelist_head|Puzzlelist_tail],
	(
      PuzzleHead = -1
	  ->
	  (
		valid_sudoku_value(Boxsize, Puzzlelist_head1)
		->  Puzzlelist_head = Puzzlelist_head1,
	    puzzle_list(PuzzleTail,Boxsize, Puzzlelist_tail)
		;
	    Puzzlelist_head = [PuzzleHead],
	    puzzle_list(PuzzleTail,Boxsize, Puzzlelist_tail)
	  )
	  ;
	    Puzzlelist_head = [PuzzleHead],
	    puzzle_list(PuzzleTail,Boxsize, Puzzlelist_tail)
	)
	).

%% Convert the puzzle from  list(list) into list(int) form	
:-  pred list_puzzle(list(list(int))::in, list(int)::out) is semidet.

list_puzzle(PuzzleList , Puzzle):-
	PuzzleList = []
	-> Puzzle = []
	;
	(  PuzzleList=[ListHead|ListTail],
	   Puzzle = [PuzzleHead|PuzzleTail],
	   (
	   list.length(ListHead) = 1
	   ->
	   list.index0(ListHead,0,PuzzleHead),
	   list_puzzle(ListTail, PuzzleTail)
	  ;
	   PuzzleHead = -1,
	   list_puzzle(ListTail, PuzzleTail)
	   )
	).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
%  Count one element(known cell) number in the puzzle_list
:- pred onelen(list(list(int))::in,int::in,int::out) is semidet.

onelen(Puzzlelist,InitLen,FinalLen):-
	Puzzlelist = []
	->
	FinalLen = InitLen
	;
	(
	Puzzlelist = [PuzzleHead|PuzzleTail],
	(
	 list.length(PuzzleHead)=1
	 ->
	 (
		InitLen1 = InitLen+1,
		onelen(PuzzleTail,InitLen1,FinalLen)
	 )
	 ;
	 onelen(PuzzleTail,InitLen,FinalLen)
	)
	).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
:- pred valid_sudoku_size(int::in, int::out, int::out) is semidet.
%  valid_sudoku_size(Size, Width, Boxsize)
%  holds if Width x Width is a valid size for a Sudoku puzzle, Size is
%  Width x Width, and Boxsize is the square root of Width.

%  This predicate is get from sudoku-starter.m written by Peter Schachte

valid_sudoku_size( 16, 4, 2).
valid_sudoku_size( 81, 9, 3).
valid_sudoku_size(256, 16, 4).
valid_sudoku_size(625, 25, 5).

:- pred valid_sudoku_value(int::in,list(int)::out) is semidet.
%  valid_sudoku_value(Boxsize, Valid value list)

valid_sudoku_value(2,[1,2,3,4]).
valid_sudoku_value(3,[1,2,3,4,5,6,7,8,9]).
valid_sudoku_value(4,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]).
valid_sudoku_value(5,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,
		17,18,19,20,21,22,23,24,25]).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Below are get from sudoku-starter.m written by Peter Schachte
							
%% cell_value_list is used to store the undetermined cell possible value list
%% :- pred cell_value_list(int::in,int::in,list(int)::out) is semidet.

:- pred load_puzzle(list(int)::out, io::di, io::uo) is det.

%  Read in a Sudoku puzzle from the current input stream and return
%  it.  We ignore the way the input is broken into lines and simply
%  return the content as a flat list of values, with -1 used for
%  un-filled cells.

load_puzzle(Puzzle, !IO) :-
	io.read_char(Result, !IO),
	(   ( Result = eof ; Result = error(_) ),
	    Puzzle = []
	;   Result = ok(Char),
	    (   char.digit_to_int(Char, Int)
	    ->  Puzzle = [Int|Puzzle1]
	    ;   % for flexibility, we accept spaces, underscores and
		% periods as indicating an unfilled cell.
		( Char = ' ' ; Char = ('.') ; Char = '_' )
	    ->  Puzzle = [-1|Puzzle1]
	    ;   Puzzle = Puzzle1
	    ),
	    load_puzzle(Puzzle1, !IO)
	).


:- pred print_puzzle(list(int)::in, int::in, int::in,
		     io::di, io::uo) is det.
%  print_puzzle(Puzzle, Size, Boxsize, !IO)
%  Print out a (possibly partially filled) sudoku puzzle
print_puzzle(Puzzle, Size, Boxsize, !IO) :-
	print_hbar(Size, Boxsize, !IO),
	(   Puzzle = []
	->  true
	;   print_chunk(Puzzle, Puzzle1, Boxsize, Size, Boxsize, !IO),
	    print_puzzle(Puzzle1, Size, Boxsize, !IO)
	).


:- pred print_chunk(list(int)::in, list(int)::out,
		    int::in, int::in, int::in, io::di, io::uo) is det.

%  Print out one Boxsize-height chunk of the given puzzle.

print_chunk(!Puzzle, Rowsleft, Size, Boxsize, !IO) :-
	(   Rowsleft = 0
	->  true
	;   print_row(!Puzzle, Size, Boxsize, !IO),
	    print_chunk(!Puzzle, Rowsleft-1, Size, Boxsize, !IO)
	).


:- pred print_row(list(int)::in, list(int)::out,
		    int::in, int::in, io::di, io::uo) is det.

%  Print out one row of the given puzzle.

print_row(!Puzzle, Remaining, Boxsize, !IO) :-
	(   0 = Remaining mod Boxsize
	->  write_char('|', !IO)
	;   true
	),
	(   Remaining = 0
	->  nl(!IO)
	;   !.Puzzle = [Int|!:Puzzle]
	->  (   int_to_digit(Int, Digit)
	    ->  write_char(Digit, !IO)
	    ;   write_char('.', !IO)
	    ),
	    print_row(!Puzzle, Remaining-1, Boxsize, !IO)
	;   nl(!IO)
	).


:- pred print_hbar(int::in, int::in, io::di, io::uo) is det.

%  print_hbar(Width, Boxsize, !IO)
%  Print out a horizontal bar of Width '-' characters punctuated by a '+'
%  every Boxsize characters and beginning and ending with a '+'.

print_hbar(Remaining, Boxsize, !IO) :-
	(   0 = Remaining mod Boxsize
	->  write_char('+', !IO)
	;   true
	),
	(   Remaining = 0
	->  nl(!IO)
	;   write_char('-', !IO),
	    print_hbar(Remaining-1, Boxsize, !IO)
	).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%	End of File: sudoku.m	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	