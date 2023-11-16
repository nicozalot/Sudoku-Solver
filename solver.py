import numpy as np
import pandas as pd

def initializeGuess(board):
    
    '''
    Initialised guess 2D array which includes lists from 1 to 9 in places where
    the board has -1 in them.
    '''
    
    dim=np.shape(board)[0]
    guess=np.empty_like(board,dtype=list)
    
    for i in range(dim):
        for j in range(dim):
            if board[i,j]!=-1:
                guess[i,j]=[]
            else:
                guess[i,j]=list(range(1,dim+1))
                
    return guess


def checkAlongDimension(board1D,candidates):
    
    ''' 
    Expects a 1D array taken form the board and checks if the candidate is present in them
    and removes him if so. I have to clone the candidate list beforehand to not interfere 
    with the looping.
    '''
    # Slicing required to create a geniune clone
    candidatesClone=candidates[:]
    
    for candidate in candidatesClone:
        if candidate in board1D:
            candidates.remove(candidate)
        

def updateGuessField(board,guess,x,y):
    
    '''
    For one given guess entry it updates this entry by removing forbidden values
    by checking column-, row- and square-wise
    '''
    
    candidates=guess[x,y]
    
    # Column wise check
    checkAlongDimension(board[:,y],candidates)
    
    # Row-wise check
    checkAlongDimension(board[x,:],candidates)
    
    # Square-wise check
    # dimensions relevant here
    dim=np.shape(board)[0]
    squareWidth=int(np.sqrt(dim))
    xlower=x-x%squareWidth
    ylower=y-y%squareWidth
    checkAlongDimension(board[xlower:xlower+squareWidth,ylower:ylower+squareWidth].flatten(),candidates)
    
    
def updateAllGuesses(board,guess):
    
    '''
    Updates all guesses by looping over the whole board.
    '''
    
    dim=np.shape(board)[0]
    
    for i in range(dim):
        for j in range(dim):
            updateGuessField(board,guess,i,j)
            
                  
            
def lookForOneEntryLists(guess):
    
    '''
    Within the guess array, check if there are any low-hanging fruits where the guess array has
    lengths 1, meaning I can just put that value into the board array.
    '''
    
    dim=np.shape(guess)[0]
    
    idx=None
    
    for i in range(dim):
        for j in range(dim):
            if len(guess[i,j])==1:
                return (i,j)
            
    # For later: raise error if no 1-entry list has been found:
    raise ValueError("No 1-entry list has been found!")
    
    
def updateBoardWithFirstGuesses(board,guess):
    
    '''
    Updates the board with the first absolutely true guess found by searching for guess lists
    of length one.
    '''
    
    try:
        idx=lookForOneEntryLists(guess)
    except ValueError:
        # this happens if no 1-entry list element has been found.
        # can be solved by applying naked pairs.
        return False
   
    # Put that guess into the board
    board[idx]=guess[idx][0]
    return True
    
    
def checkIfDone(board):
    
    '''
    Checks is a board is solved.
    '''
    
    dim=np.shape(board)[0]
    
    for i in range(dim):
        for j in range(dim):
            if board[i,j]==-1:
                return False
            
    return True
            
    
    
def nakedPairColumn(guess,col):
    
    '''
    First: find an element that is of length 2, then check if there's a brother, then 
    remove in the other entries
    '''

    dim=np.shape(guess)[0]
    
    guess1D=guess[:,col]
    
    for i in range(dim):
        if len(guess1D[i])==2:
            # now we have at least one element of length 2. does it have a partner?
            for j in range(dim):
                if i!=j and guess1D[i]==guess1D[j]:
                    # naked pair found. column is col, entries are i and j. Remove in the rest.
                    #print("found in col")
                    for k in range(dim):
                        if k!=i and k!=j:
                            # now loop over the guess values of the naked pair and remove them
                            for nakedVal in guess1D[i]:
                                try:
                                    guess[k,col].remove(nakedVal)
                                    #print("Removed naked pair", guess1D[i])
                                except ValueError:
                                    whattodohere=0
                                    
                                    
def nakedPairRow(guess,row):
    '''
    First: find an element that is of length 2, then check if there's a brother, then 
    remove in the other entries
    '''

    dim=np.shape(guess)[0]
    
    guess1D=guess[row,:]
    
    for i in range(dim):
        if len(guess1D[i])==2:
            # now we have at least one element of length 2. does it have a partner?
            for j in range(dim):
                if i!=j and guess1D[i]==guess1D[j]:
                    # naked pair found. row is row, entries are i and j. Remove in the rest.
                    #print("found in row")
                    for k in range(dim):
                        if k!=i and k!=j:
                            # now loop over the guess values of the naked pair and remove them
                            for nakedVal in guess1D[i]:
                                try:
                                    guess[row,k].remove(nakedVal)
                                    #print("Removed naked pair", guess1D[i])
                                except ValueError:
                                    whattodohere=0

                                    
def nakedPairSquare(guess,identifier):
    
    '''
    Find naked pairs in given squares.
    '''
    
    dim=np.shape(guess)[0]
    squareWidth=int(np.sqrt(dim))
    
    lower=identifier-identifier%squareWidth
    
    # loop over all square elements
    for i in range(lower,lower+squareWidth):
        for j in range(lower,lower+squareWidth):
            if len(guess[i,j])==2:
                #look for duplicates
                for k in range(lower,lower+squareWidth):
                    for l in range(lower,lower+squareWidth):
                        if (i,j)!=(k,l) and guess[i,j]==guess[k,l]:
                            # cool, i found a naked prime. remove it in the other entries.
                            #print("found in sqaure")
                            for nakedVal in guess[i,j]:
                                # loop over the other entires
                                for x in range(lower,lower+squareWidth):
                                    for y in range(lower,lower+squareWidth):
                                        if (x,y)!=(i,j) and (x,y)!=(k,l):
                                            try:
                                                guess[x,y].remove(nakedVal)
                                                #print("Removed naked pair", guess[i,j])
                                            except ValueError:
                                                whattodohere=0
        
    
def removeAllNakedPairs(guess):
    
    '''
    Removes naked squares for all columns, rows and squares
    '''
    
    dim=np.shape(guess)[0]
    squareWidth=int(np.sqrt(dim))
    
    for i in range(dim):
        nakedPairColumn(guess,i)
        nakedPairRow(guess,i)
        nakedPairSquare(guess,i)
        
        
        

def singleInCol(board,guess,col):
    
    '''
    Checks along a given column whether there are any numbers which occur only once within that 
    guess column. If so, it sets the value and updates the whole guess array.
    '''
    
    dim=np.shape(guess)[0]
    
    board1D=board[:,col]
    guess1D=guess[:,col]
    
    
    # Loop over possible numbers:
    for num in range(1,dim+1):
        # loop over the items and check how often that number appears
        counter=0
        for i in range(dim):
            if num in guess1D[i]:
                counter+=1
                idx=i
        
        # If only found once: then it must be in the respective field.
        if counter==1:
            board[idx,col]=num
            guess[idx,col]=[]
            #print("found single in col",col)
            updateAllGuesses(board,guess)
        

            
def singleInRow(board,guess,row):
    
    '''
    Checks along a given row whether there are any numbers which occur only once within that 
    guess column. If so, it sets the value and updates the whole guess array.
    '''
    
    dim=np.shape(guess)[0]
    
    board1D=board[row,:]
    guess1D=guess[row,:]
    
    
    # Loop over possible numbers:
    for num in range(1,dim+1):
        # loop over the items and check how often that number appears
        counter=0
        for i in range(dim):
            if num in guess1D[i]:
                counter+=1
                idx=i
        
        # If only found once: then it must be in the respective field.
        if counter==1:
            board[row,idx]=num
            guess[row,idx]=[]
            #print("found single in row. Updated entry",row,idx)
            updateAllGuesses(board,guess)
            
    
    
def singleInSquare(board,guess,identifier):
    
    '''
    Checks in a given square whether there are any numbers which occur only once within that 
    guess column. If so, it sets the value and updates the whole guess array.
    '''
    
    dim=np.shape(guess)[0]
    squareWidth=int(np.sqrt(dim))
    
    lower=identifier-identifier%squareWidth

    # Loop over possible numbers:
    for num in range(1,dim+1):
        counter=0
        for i in range(lower,lower+squareWidth):
            for j in range(lower,lower+squareWidth):
                if num in guess[i,j]:
                    counter+=1
                    idx=(i,j)
                    
        # If only found once: then it must be in the respective field.
        if counter==1:
            board[idx]=num
            guess[idx]=[]
            #print("found single in square")
            updateAllGuesses(board,guess)
            
    

    
def checkAllSingles(board,guess):
    
    '''
    Checks for singles in columns, rows and squares.
    '''
    
    dim=np.shape(guess)[0]
    
    for i in range(dim):
        singleInCol(board,guess,i)
        singleInRow(board,guess,i)
        singleInSquare(board,guess,i)
            
            
def countGuessEntriesOfLengthN(guess,N):
    
    '''
    Returns how many entries with length less or equal N are in guess array and their respective
    positions.
    '''
    
    dim=np.shape(guess)[0]
    counter=0
    
    idxes=[]
    for i in range(dim):
        for j in range(dim):
            if len(guess[i,j])<=N:
                counter+=1
                idxes.append((i,j))
                    
    return counter,idxes
            

    
def guessPlausible(board,guess):
    
    '''
    Checks if there are any board entries which haven't been filled for which no guesses are
    available. If that is the case, the function returns False, otherwise True.
    '''
    
    dim=np.shape(guess)[0]
    
    for i in range(dim):
        for j in range(dim):
            if board[i,j]==-1 and len(guess[i,j])==0:
                return False
   
    return True


def alternativeBoardSolutionPossible(board):
    
    '''
    Checks if the board can be solved (without further guessing) in its current state by 
    evaluating the plausibility of the guess array and if plausible trying to solve
    the board without further guessing, which would blow up the code and isn't really required
    in order to solve even the hardest Sudokus. I'd imagine this can be implemented for even more
    difficult Sudokus (which I haven't encountered yet...)
    '''
    
    boardSave=None
    
    # just do an adapted form of sudoku solver.
    while not checkIfDone(board):
        # Initialize the guess array
        guess=initializeGuess(board)
        
        # Update all guesses
        updateAllGuesses(board,guess)
        
        # Check if guess makes sense.
        if not guessPlausible(board,guess):
            #print("inconsitency found")
            return False

        # Remove all naked pairs.
        removeAllNakedPairs(guess)

        # Check all Singles
        checkAllSingles(board,guess)

        # Update the board according to the 1-level guesses
        updateSuccess1Level=updateBoardWithFirstGuesses(board,guess)

        # Check if progress has been made
        if type(boardSave)!=type(None) and (boardSave==board).all():
            #print("Path is leading nowhere.")
            return False
                
        boardSave=np.copy(board)
        
    #print(board)
    #print("board solved, returning true")
    return True
                
                 
    
def startGuessing(board,guess):
    
    '''
    Find out where easy targets are where guess length is less or equal than 2.
    The number 2 has been hard coded, but can be increased if required.
    Loop over all of of the easy targets. Update copy of guess board accordingly. 
    Try to solve this alternative board. If it's possible and a solution has been found, update
    the original board. (This makes sense since each Sudoku only have one solution)
    '''
    
    dim=np.shape(guess)[0]
    counter,idxes=countGuessEntriesOfLengthN(guess,2)
    
    # Loop over all idxes.
    for idx in idxes:
        # Loop over the possible entries
        for entry in guess[idx]:
            #print(f"Guessing {entry} in field {idx}") 

            boardCopy=np.copy(board)  
            
            # Update board copy
            boardCopy[idx]=entry   
            
            # Continue with alternative board.
            if alternativeBoardSolutionPossible(boardCopy):
                board[idx]=entry
                #print(f"putting {entry} in field {idx}")

            
            
def sudokuSolver(board):
    
    '''
    The master script that solves a board trying all of the below methods step by step.
    '''
    
    counter=0
    print(end="\r")
    
    while not checkIfDone(board):
        # Initialize the guess array
        guess=initializeGuess(board)

        # Update all guesses
        updateAllGuesses(board,guess)

        # Remove all naked pairs.
        removeAllNakedPairs(guess)
        
        # Check all Singles
        checkAllSingles(board,guess)
        
        # Update the board according to the 1-level guesses
        updateSuccess1Level=updateBoardWithFirstGuesses(board,guess)
        
        
        if counter>0 and (boardSave==board).all():
            # Check if there are any items of length  less or equal to 2 and start guessing.
            if countGuessEntriesOfLengthN(guess,2)[0]>0:
                #print("started guessing")
                startGuessing(board,guess)
                
                # if even guessing cannot change board: stop.
                if (boardSave==board).all():
                    raise RuntimeError(f"Board unchanged even after guessing! Stopped in step {counter}.")
        
        # save current state
        boardSave=np.copy(board)

        limit=1e3
        if counter>limit:
            raise RuntimeError(f"More than {limit} tries, aborting.")
        
        print(f"Round {counter}",end="\r")
        counter+=1
    print()
