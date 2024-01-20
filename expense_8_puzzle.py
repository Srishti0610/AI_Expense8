import sys

import datetime

# print(sys.argv)
startFile = sys.argv[1]
goalFile = sys.argv[2]
algorithm = sys.argv[3]

# function to choose algorithm
def chosenAlgirithm(case):
    if case == "dfs":
        DFS(startMatrix)
    elif case == "bfs":
        BFS(startMatrix)
    elif case == "ucs":
        UCS(startMatrix)
    elif case == "ids":
        IDS(startMatrix)
    elif case == "greedy":
        Greedy(startMatrix)
    elif case == "dls":
        DLS(startMatrix)
    else:
        AstarSolve(startMatrix)



# Initialize an empty matrix for input
startMatrix = []
goalMatrix = []

def readFile(filename, matrix):
    # Open the file for reading
    with open(filename, 'r') as file:
        for line in file:
            # Check if the line is "END OF FILE," and if it is, break out of the loop
            if line.strip() == "END OF FILE":
                break
            # Split the line into elements using space as a separator and convert them to integers
            row = [int(num) for num in line.split()]
            # Append the row to the matrix
            matrix.append(row)

readFile(startFile, startMatrix)
readFile(goalFile, goalMatrix)
print("Start Matrix",startMatrix)
print("Goal Matrix",goalMatrix)


# Calculate the heuristic of the current matrix
def calculateHeuristic(currentState):
    heuristic = 0
    for i in range(3):
        for j in range(3):
            if currentState[i][j] != 0:  # Supposed to be the blank tile
                goal_position = None
                for x in range(3):
                    if goalMatrix[x].count(currentState[i][j]) > 0:
                        goal_position = (x, goalMatrix[x].index(currentState[i][j]))
                        break
                heuristic += abs(i - goal_position[0])*currentState[i][j] + abs(j - goal_position[1])*currentState[i][j]
    return heuristic


# Find the position of 0 in the matrix
def positionFinder(currentState, num):
    for i in range(3):
        for j in range(3):
            if currentState[i][j] == num:
                return i, j
    return None



# Check if a move is valid
def moveValidity(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Find possible moves for 0
movesList = [(0, 1), (0, -1),(1, 0), (-1, 0)] # represents right, left, down, up
alldirections={(0,1):"left",(0,-1):"right",(1,0):"up",(-1,0):"down"} # opposite because its in tems of the number moved


# Check if the states match
def matchGoalState(currentMatrix):
    return currentMatrix==goalMatrix

# Define sort function
def listSort(item):
    return item["fn"]


def listSortGreedy(item):
    return item["hn"]


def listSortUCS(item):
    return item["gn"]

# Astar
def findPossibleMovesAstar(startMatrix, i ,j, gn, path):
    newGeneratedState = []
    for move in movesList:
        moved_i, moved_j = i + move[0], j + move[1]
        
        if moveValidity(moved_i, moved_j):
            newState = [list(row) for row in startMatrix]  # Copy the current state
            newState[i][j], newState[moved_i][moved_j] = newState[moved_i][moved_j], newState[i][j]  # Perform the move
            heuristicValue=calculateHeuristic(newState)
            newGeneratedState.append({
                "generatedMatrix":newState,
                "numMoved":newState[i][j],
                "path":path+["Move "+str(newState[i][j]) +" "+ str(alldirections[move])],
                "action":alldirections[move],
                "gn":gn+newState[i][j],
                "hn":heuristicValue,
                "fn":gn+newState[i][j]+heuristicValue}
                )
            #state matrix, numebr moved or gn, direction, hn, fn
    return newGeneratedState

def AstarSolve(startMatrix):
    nodesGenerated = [startMatrix]
    closedSet =[]
    popped=0
    queue = [{
        "stateMatrix": startMatrix,
        "path":[],
        "parent":None,
        "depth":0,
        "gn":0, 
        "hn":calculateHeuristic(startMatrix), 
        "fn":calculateHeuristic(startMatrix)
        }] 
    # current state, path, parent, depth, gn, hn, fn
    
    if len(sys.argv) >= 5:
        if(sys.argv[4]=="true"):
            getdatetime = datetime.datetime.now()

            # Format the date and time as needed
            date_ = getdatetime.strftime("%Y-%m-%d")
            time_ = getdatetime.strftime("%H-%M-%S")

            # Create the file name using the format
            file_name = f"trace-{date_}-{time_}.txt"
            dumpFile = open(file_name, "w")
            dumpFile.write(f"Command Line arguments {sys.argv}:\n")
            dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
            dumpFile.write(f"Running :{algorithm}\n")
    dumpFileData = ""
    while queue:
        values = list(queue.pop(0).values())
        currentState, path, parent, depthVal, gn, hn, fn = values
        popped+=1
        if matchGoalState(currentState):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution Found at depth ", depthVal, " with cost of ", fn)
            print("Steps: ")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution Found at depth : {depthVal} with cost of {fn}\n")
            dumpFileData+=(f"Steps:\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        
        if(currentState not in closedSet):
            closedSet.append(currentState)

            i, j = positionFinder(currentState, 0)
            # print(i,j)
            generatedState = findPossibleMovesAstar(currentState, i, j, gn, path)
            generatedState = sorted(generatedState, key=listSort)
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                    dumpFile.write(f"\tClosed = {closedSet}\n")
                    dumpFile.write(f"\t{len(generatedState)} successors generated\n")
            for state in generatedState:
                nodesGenerated.append(state['generatedMatrix'])
                queue.append({
                "stateMatrix": state['generatedMatrix'],
                "path":state['path'],
                "parent":currentState,
                "depth":depthVal+1,
                "gn":state['gn'], 
                "hn":state['hn'], 
                "fn":state['fn']
                })
        queue = sorted(queue, key=listSort)
        
        if len(sys.argv) >= 5:
            if(sys.argv[4]=="true"):
                dumpFile.write(f"Fringe:  \n")
                for frin in queue:
                    dumpFile.write(f"\t {str(frin)} \n")

    return None

# Greedy
def findPossibleMovesGreedy(startMatrix, i ,j, path):
    newGeneratedState = []
    for move in movesList:
        moved_i, moved_j = i + move[0], j + move[1]
        
        if moveValidity(moved_i, moved_j):
            newState = [list(row) for row in startMatrix]  # Copy the current state
            newState[i][j], newState[moved_i][moved_j] = newState[moved_i][moved_j], newState[i][j]  # Perform the move
            heuristicValue=calculateHeuristic(newState)
            newGeneratedState.append({
                "generatedMatrix":newState,
                "numMoved":newState[i][j],
                "path":path+["Move "+str(newState[i][j]) +" "+ str(alldirections[move])],
                "action":alldirections[move],
                "hn":heuristicValue
                }
                )
            #state matrix, numebr moved or gn, direction, hn, fn
    return newGeneratedState

def Greedy(startMatrix):
    nodesGenerated = [startMatrix]
    closedSet =[]
    popped=0
    queue = [{
        "stateMatrix": startMatrix,
        "path":[],
        "parent":None,
        "depth":0,
        "hn":calculateHeuristic(startMatrix)
        }] 
    # current state, path, parent, depth, gn, hn, fn
    
    if len(sys.argv) >= 5:
        if(sys.argv[4]=="true"):
            getdatetime = datetime.datetime.now()

            # Format the date and time as needed
            date_ = getdatetime.strftime("%Y-%m-%d")
            time_ = getdatetime.strftime("%H-%M-%S")

            # Create the file name using the format
            file_name = f"trace-{date_}-{time_}.txt"
            dumpFile = open(file_name, "w")
            dumpFile.write(f"Command Line arguments {sys.argv}:\n")
            dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
            dumpFile.write(f"Running :{algorithm}\n")
    dumpFileData = ""
    while queue:
        values = list(queue.pop(0).values())
        currentState, path, parent, depthVal, hn = values
        popped+=1
        if matchGoalState(currentState):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution Found at depth ", depthVal, " with cost of ", hn)
            print("Steps: ")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution Found at depth : {depthVal} with cost of {hn}\n")
            dumpFileData+=(f"Steps:\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        
        if(currentState not in closedSet):
            closedSet.append(currentState)

            i, j = positionFinder(currentState, 0)
            # print(i,j)
            generatedState = findPossibleMovesGreedy(currentState, i, j, path)
            generatedState = sorted(generatedState, key=listSortGreedy)
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                    dumpFile.write(f"\tClosed = {closedSet}\n")
                    dumpFile.write(f"\t{len(generatedState)} successors generated\n")
            for state in generatedState:
                nodesGenerated.append(state['generatedMatrix'])
                queue.append({
                "stateMatrix": state['generatedMatrix'],
                "path":state['path'],
                "parent":currentState,
                "depth":depthVal+1,
                "hn":state['hn']
                })
        queue = sorted(queue, key=listSortGreedy)
        
        if len(sys.argv) >= 5:
            if(sys.argv[4]=="true"):
                dumpFile.write(f"Fringe:  \n")
                for frin in queue:
                    dumpFile.write(f"\t {str(frin)} \n")

    return None

# UCS
def findPossibleMovesUCS(startMatrix, i ,j, gn, path):
    newGeneratedState = []
    for move in movesList:
        moved_i, moved_j = i + move[0], j + move[1]
        
        if moveValidity(moved_i, moved_j):
            newState = [list(row) for row in startMatrix]  # Copy the current state
            newState[i][j], newState[moved_i][moved_j] = newState[moved_i][moved_j], newState[i][j]  # Perform the move
            heuristicValue=calculateHeuristic(newState)
            newGeneratedState.append({
                "generatedMatrix":newState,
                "numMoved":newState[i][j],
                "path":path+["Move "+str(newState[i][j]) +" "+ str(alldirections[move])],
                "action":alldirections[move],
                "gn":gn+newState[i][j]
                }
                )
            #state matrix, numebr moved or gn, direction, hn, fn
    return newGeneratedState

def UCS(startMatrix):
    nodesGenerated = [startMatrix]
    closedSet =[]
    popped=0
    queue = [{
        "stateMatrix": startMatrix,
        "path":[],
        "parent":None,
        "depth":0,
        "gn":0
        }] 
    # current state, path, parent, depth, gn, hn, fn
    
    if len(sys.argv) >= 5:
        if(sys.argv[4]=="true"):
            getdatetime = datetime.datetime.now()

            # Format the date and time as needed
            date_ = getdatetime.strftime("%Y-%m-%d")
            time_ = getdatetime.strftime("%H-%M-%S")

            # Create the file name using the format
            file_name = f"trace-{date_}-{time_}.txt"
            dumpFile = open(file_name, "w")
            dumpFile.write(f"Command Line arguments {sys.argv}:\n")
            dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
            dumpFile.write(f"Running :{algorithm}\n")
    dumpFileData = ""
    while queue:
        values = list(queue.pop(0).values())
        currentState, path, parent, depthVal, gn = values
        popped+=1
        if matchGoalState(currentState):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution Found at depth ", depthVal, " with cost of ", gn)
            print("Steps: ")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution Found at depth : {depthVal} with cost of {gn}\n")
            dumpFileData+=(f"Steps:\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        
        if(currentState not in closedSet):
            closedSet.append(currentState)

            i, j = positionFinder(currentState, 0)
            # print(i,j)
            generatedState = findPossibleMovesUCS(currentState, i, j, gn, path)
            generatedState = sorted(generatedState, key=listSortUCS)
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                    dumpFile.write(f"\tClosed = {closedSet}\n")
                    dumpFile.write(f"\t{len(generatedState)} successors generated\n")
            for state in generatedState:
                nodesGenerated.append(state['generatedMatrix'])
                queue.append({
                "stateMatrix": state['generatedMatrix'],
                "path":state['path'],
                "parent":currentState,
                "depth":depthVal+1,
                "gn":state['gn']
                })
            queue = sorted(queue, key=listSortUCS)
            
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"Fringe:  \n")
                    for frin in queue:
                        dumpFile.write(f"\t {str(frin)} \n")

    return None

def findPossibleMoves(startMatrix, i ,j, path):
    newGeneratedState = []
    for move in movesList:
        moved_i, moved_j = i + move[0], j + move[1]
        
        if moveValidity(moved_i, moved_j):
            newState = [list(row) for row in startMatrix]  # Copy the current state
            newState[i][j], newState[moved_i][moved_j] = newState[moved_i][moved_j], newState[i][j]  # Perform the move
            newGeneratedState.append({
                "generatedMatrix":newState,
                "numMoved":newState[i][j],
                "path":path+["Move "+str(newState[i][j]) +" "+ str(alldirections[move])],
                "action":alldirections[move],
                }
                )
            #state matrix, numebr moved or gn, direction, hn, fn
    return newGeneratedState


# BFS
def BFS(startMatrix):
    nodesGenerated = [startMatrix]
    closedSet =[]
    popped=0
    queue = [{
        "stateMatrix": startMatrix,
        "path":[],
        "parent":None,
        "depth":0
        }] 
    # current state, path, parent, depth, gn, hn, fn
    
    if len(sys.argv) >= 5:
        if(sys.argv[4]=="true"):
            getdatetime = datetime.datetime.now()

            # Format the date and time as needed
            date_ = getdatetime.strftime("%Y-%m-%d")
            time_ = getdatetime.strftime("%H-%M-%S")

            # Create the file name using the format
            file_name = f"trace-{date_}-{time_}.txt"
            dumpFile = open(file_name, "w")
            dumpFile.write(f"Command Line arguments {sys.argv}:\n")
            dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
            dumpFile.write(f"Running :{algorithm}\n")
    dumpFileData = ""
    while queue:
        values = list(queue.pop(0).values())
        currentState, path, parent, depthVal = values
        popped+=1
        if matchGoalState(currentState):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution Found at depth ", depthVal)
            print("Steps: ")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution Found at depth : {depthVal} \n")
            dumpFileData+=(f"Steps:\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        
        if(currentState not in closedSet):
            closedSet.append(currentState)

            i, j = positionFinder(currentState, 0)
            # print(i,j)
            generatedState = findPossibleMoves(currentState, i, j, path)
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                    dumpFile.write(f"\tClosed = {closedSet}\n")
                    dumpFile.write(f"\t{len(generatedState)} successors generated\n")
            for state in generatedState:
                nodesGenerated.append(state['generatedMatrix'])
                queue.append({
                "stateMatrix": state['generatedMatrix'],
                "path":state['path'],
                "parent":currentState,
                "depth":depthVal+1
                })
        
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"Fringe:  \n")
                    for frin in queue:
                        dumpFile.write(f"\t {str(frin)} \n")

    return None

# DFS
def DFS(startMatrix):
    nodesGenerated = [startMatrix]
    closedSet =[]
    popped=0
    queue = [{
        "stateMatrix": startMatrix,
        "path":[],
        "parent":None,
        "depth":0
        }] 
    # current state, path, parent, depth, gn, hn, fn
    
    if len(sys.argv) >= 5:
        if(sys.argv[4]=="true"):
            getdatetime = datetime.datetime.now()

            # Format the date and time as needed
            date_ = getdatetime.strftime("%Y-%m-%d")
            time_ = getdatetime.strftime("%H-%M-%S")

            # Create the file name using the format
            file_name = f"trace-{date_}-{time_}.txt"
            dumpFile = open(file_name, "w")
            dumpFile.write(f"Command Line arguments {sys.argv}:\n")
            dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
            dumpFile.write(f"Running :{algorithm}\n")
    dumpFileData = ""
    while queue:
        values = list(queue.pop().values())
        currentState, path, parent, depthVal = values
        popped+=1
        if matchGoalState(currentState):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution Found at depth ", depthVal)
            print("Steps: ")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution Found at depth : {depthVal} \n")
            dumpFileData+=(f"Steps:\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        
        if(currentState not in closedSet):
            closedSet.append(currentState)

            i, j = positionFinder(currentState, 0)
            # print(i,j)
            generatedState = findPossibleMoves(currentState, i, j, path)
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                    dumpFile.write(f"\tClosed = {closedSet}\n")
                    dumpFile.write(f"\t{len(generatedState)} successors generated\n")
            for state in generatedState:
                nodesGenerated.append(state['generatedMatrix'])
                queue.append({
                "stateMatrix": state['generatedMatrix'],
                "path":state['path'],
                "parent":currentState,
                "depth":depthVal+1
                })
        
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"Fringe:  \n")
                    for frin in queue:
                        dumpFile.write(f"\t {str(frin)} \n")

    return None

# DLS
def DLS(startMatrix):
    depthLimit = int(input("Enter the depth limit"))
    nodesGenerated = [startMatrix]
    closedSet =[]
    popped=0
    queue = [{
        "stateMatrix": startMatrix,
        "path":[],
        "parent":None,
        "depth":0
        }] 
    # current state, path, parent, depth, gn, hn, fn
    
    if len(sys.argv) >= 5:
        if(sys.argv[4]=="true"):
            getdatetime = datetime.datetime.now()

            # Format the date and time as needed
            date_ = getdatetime.strftime("%Y-%m-%d")
            time_ = getdatetime.strftime("%H-%M-%S")

            # Create the file name using the format
            file_name = f"trace-{date_}-{time_}.txt"
            dumpFile = open(file_name, "w")
            dumpFile.write(f"Command Line arguments {sys.argv}:\n")
            dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
            dumpFile.write(f"Running :{algorithm}\n")
    dumpFileData = ""
    while queue:
        values = list(queue.pop().values())
        currentState, path, parent, depthVal = values
        popped+=1
        if (depthVal >= depthLimit):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution not found")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution not found\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        if matchGoalState(currentState):
            print("Nodes Popped" ,(popped))
            print("Nodes Expanded" ,len(closedSet))
            print("Nodes Generated" ,len(nodesGenerated))
            print("Max Fringe Size" ,len(queue)+1)
            print("Solution Found at depth ", depthVal)
            print("Steps: ")
            dumpFileData+=(f"Nodes Popped: {popped}\n")
            dumpFileData+=(f"Nodes Expanded: {len(closedSet)}\n")
            dumpFileData+=(f"Nodes Generated: {len(nodesGenerated)}\n")
            dumpFileData+=(f"Max Fringe Size: {len(queue)+1}\n")
            dumpFileData+=(f"Solution Found at depth : {depthVal} \n")
            dumpFileData+=(f"Steps:\n")
            for pathtrav in path:
                print(pathtrav)
                dumpFileData+=(f"{pathtrav}\n")
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(dumpFileData)
            return
        
        if(currentState not in closedSet):
            closedSet.append(currentState)

            i, j = positionFinder(currentState, 0)
            # print(i,j)
            generatedState = findPossibleMoves(currentState, i, j, path)
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                    dumpFile.write(f"\tClosed = {closedSet}\n")
                    dumpFile.write(f"\t{len(generatedState)} successors generated\n")
            for state in generatedState:
                nodesGenerated.append(state['generatedMatrix'])
                queue.append({
                "stateMatrix": state['generatedMatrix'],
                "path":state['path'],
                "parent":currentState,
                "depth":depthVal+1
                })
        
            if len(sys.argv) >= 5:
                if(sys.argv[4]=="true"):
                    dumpFile.write(f"Fringe:  \n")
                    for frin in queue:
                        dumpFile.write(f"\t {str(frin)} \n")

    return None

# IDS
def IDS(startMatrix):

    if len(sys.argv) >= 5 and sys.argv[4] == "true":
        getdatetime = datetime.datetime.now()
        date_ = getdatetime.strftime("%Y-%m-%d")
        time_ = getdatetime.strftime("%H-%M-%S")
        file_name = f"trace-{date_}-{time_}.txt"
        dumpFile = open(file_name, "w")
        dumpFile.write(f"Command Line arguments {sys.argv}:\n")
        dumpFile.write(f"Method Selected: {sys.argv[3]}\n")
        dumpFile.write(f"Running :{algorithm}\n")

    for depth_limit in range(sys.maxsize):
        nodesGenerated = [startMatrix]
        closedSet = []
        popped = 0
        queue = [{
            "stateMatrix": startMatrix,
            "path": [],
            "parent": None,
            "depth": 0
        }]

        dumpFileData = ""
        while queue:
            values = list(queue.pop().values())
            currentState, path, parent, depthVal = values
            popped += 1
            if matchGoalState(currentState):
                print("Nodes Popped", (popped))
                print("Nodes Expanded", len(closedSet))
                print("Nodes Generated", len(nodesGenerated))
                print("Max Fringe Size", len(queue) + 1)
                print("Solution Found at depth ", depthVal)
                print("Steps: ")
                dumpFileData += (f"Nodes Popped: {popped}\n")
                dumpFileData += (f"Nodes Expanded: {len(closedSet)}\n")
                dumpFileData += (f"Nodes Generated: {len(nodesGenerated)}\n")
                dumpFileData += (f"Max Fringe Size: {len(queue) + 1}\n")
                dumpFileData += (f"Solution Found at depth : {depthVal} \n")
                dumpFileData += (f"Steps:\n")
                for pathtrav in path:
                    print(pathtrav)
                    dumpFileData += (f"{pathtrav}\n")
                if len(sys.argv) >= 5 and sys.argv[4] == "true":
                    dumpFile.write(dumpFileData)
                return

            if depthVal < depth_limit:
                if currentState not in closedSet:
                    closedSet.append(currentState)
                    i, j = positionFinder(currentState, 0)
                    generatedState = findPossibleMoves(currentState, i, j, path)
                    if len(sys.argv) >= 5 and sys.argv[4] == "true":
                        dumpFile.write(f"\nGenerating successors to < {currentState} \n")
                        dumpFile.write(f"\tClosed = {closedSet}\n")
                        dumpFile.write(f"\t{len(generatedState)} successors generated\n")
                    for state in generatedState:
                        nodesGenerated.append(state['generatedMatrix'])
                        queue.append({
                            "stateMatrix": state['generatedMatrix'],
                            "path": state['path'],
                            "parent": currentState,
                            "depth": depthVal + 1
                        })

            if len(sys.argv) >= 5 and sys.argv[4] == "true":
                dumpFile.write(f"Fringe:  \n")
                for frin in queue:
                    dumpFile.write(f"\t {str(frin)} \n")

    return None




chosenAlgirithm(algorithm)