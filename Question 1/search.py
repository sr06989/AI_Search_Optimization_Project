# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
from argparse import Action
from ast import Delete, operator
import operator
from lzma import CHECK_ID_MAX
import tkinter
import csv
from turtle import st
from util import PriorityQueueWithFunction
from util import PriorityQueue
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """

        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """

        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """

        util.raiseNotDefined()

    def getHeuristic(self, state):
        """
         state: the current state of agent

         THis function returns the heuristic of current state of the agent which will be the 
         estimated distance from goal.
        """
        util.raiseNotDefined()


class JumpingFrogs(SearchProblem):
    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        self.StartState = ["L", "L", "L", "V", "R", "R", "R"]

        return self.StartState

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """

        self.GoalState = ["R", "R", "R", "V", "L", "L", "L"]

        if state == self.GoalState:
            return True

        return False

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        EmptyPosition = state.index("V")
        Length = len(state)
        Succesors = []

        if EmptyPosition-1 >= 0 and state[EmptyPosition-1] == "L":

            NewState = state.copy()

            i = EmptyPosition

            temp = NewState[i]
            NewState[i] = NewState[i - 1]
            NewState[i - 1] = temp

            Succesors.append((NewState, "LeftOnce", 1))

        if EmptyPosition - 2 >= 0 and state[EmptyPosition-2] == "L":

            NewState = state.copy()

            i = EmptyPosition

            temp = NewState[i]
            NewState[i] = NewState[i - 2]
            NewState[i - 2] = temp

            Succesors.append((NewState, "LeftTwice", 2))

        if EmptyPosition + 1 <= Length - 1 and state[EmptyPosition+1] == "R":

            NewState = state.copy()

            i = EmptyPosition

            temp = NewState[i + 1]
            NewState[i + 1] = NewState[i]
            NewState[i] = temp

            Succesors.append((NewState, "RightOnce", 2))

        if EmptyPosition + 2 <= Length - 1 and state[EmptyPosition+2] == "R":

            NewState = state.copy()

            i = EmptyPosition

            temp = NewState[i + 2]
            NewState[i + 2] = NewState[i]
            NewState[i] = temp

            Succesors.append((NewState, "RightTwice", 2))

        return Succesors

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        TotalCost = 0

        for i in actions:
            if i == "LeftOnce" or i == "RightOnce":
                TotalCost += 1
            else:
                TotalCost += 2

        return TotalCost

    def getHeuristic(self, state):
        """
         state: the current state of agent

         THis function returns the heuristic of current state of the agent which will be the 
         estimated distance from goal.
        """


        length = len(state)
        heuristic = 0

        for i in range(length):

            if i < 3:
                if state[i] != 'R':
                    heuristic = heuristic + 1

            elif i > 3:
                if state[i] != 'L':
                    heuristic = heuristic + 1

        return heuristic


class RoutePlanning(SearchProblem):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def __init__(self, start, goal, Cities, Connections, Heuristics):
        self.allcities = [] #Contains Names of all Cities
        self.columnnames_Connections = [] #Contains Column Names of Connections CSV file
        self.allconnections = {} #Dictionary of Connections where Key is the start city and its Value is the Cost to get to its Connection
        #The Name of Each of the Next States is stored in the same index in columnnames_Connections
        self.columnnames_Heuristics = [] #Contains Column Names of Heuristics CSV file
        self.allHeuristics = {} #Dictionary of Hueristics where Key is the start city and its Value is the Hueresitc to get to next State
        #The Name of Each of the Next States is stored in the same index in columnnames_Heuristics
        self.Start = start 
        self.Goal = goal

        with open(Cities, 'r') as file1:
            csvreader = csv.reader(file1)
            for row in csvreader:
                self.allcities.append(row[0])

        i = 0

        with open(Connections, 'r') as file2:
            csvreader = csv.reader(file2)
            for row1 in csvreader:
                if i == 0:
                    self.columnnames_Connections = row1[1:]
                    i += 1
                else:
                    temp = []
                    temp = row1
                    City = temp[0]
                    self.allconnections[City] = temp[1:]

        j = 0

        with open(Heuristics, 'r') as file3:
            csvreader = csv.reader(file3)
            for row2 in csvreader:
                if j == 0:
                    self.columnnames_Heuristics = row2[1:]
                    j += 1
                else:
                    temp = []
                    temp = row2
                    City = temp[0]
                    self.allHeuristics[City] = temp[1:]

        # self.getHeuristic(start)

        # print(self.allcities)
        # print(self.allconnections)
        # print(self.allHeuristics)

        # print(self.getSuccessors("Islamabad"))

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """

        return self.Start

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """

        if state == self.Goal:
            return True

        return False

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        Successors = []

        #stateposition = self.allconnections.index(state)

        allconnects = self.allconnections[state].copy() #Create a List of Every Connection that the state given has

        for i in range(len(allconnects)): 
            StepCost = allconnects[i] 
            if StepCost != "-1" and StepCost != "0": #If Cost == 0 or Cost == -1 then no Connection will exist
                Successor = self.columnnames_Connections[i] #Find name of Next State Using index
                Action = (state, Successor, StepCost) 
            #StepCost = allconnects[i]
                triple = (Successor, Action, int(StepCost))
                Successors.append(triple)

        return Successors

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        cost = 0

        for i in actions:
            cost = cost + int(i[2]) 
       
        return cost


    def getHeuristic(self, state):
        """
         state: the current state of agent

         THis function returns the heuristic of current state of the agent which will be the 
         estimated distance from goal.
        """
        goal = self.Goal 
        allHeuristics = self.allHeuristics.copy() 
        allHeuristicColumns = self.columnnames_Heuristics.copy()
        index = allHeuristicColumns.index(goal)
        h = allHeuristics[state][index]

        return int(h)


def InsertionSort(array):

    for step in range(1, len(array)):
        keylist = array[step]
        key = array[step][0]
        j = step - 1
        while j >= 0 and key < array[j][0]:
            array[j+1] = array[j]
            j = j - 1

        array[j + 1] = keylist


def aStarSearch(problem):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR A* CODE HERE ***"

    OpenList = []
    ClosedList = []
    Actions = [] 
    Path = []
    Node = problem.getStartState()

    while problem.isGoalState(Node) != True:

        Path.append(Node) 
        ClosedList.append(Node)
        neighbors = problem.getSuccessors(Node)

        for neighbor in neighbors:

            Actions.append(neighbor[1])
            ActionNames = Actions[:]

            f_n = problem.getHeuristic(neighbor[0]) + problem.getCostOfActions(Actions)

            Path.append(neighbor[0])
            PathCopy = Path[:]

            del Path[-1]
            del PathCopy[-1]
            del Actions[-1]

            temp = (f_n, neighbor[0], ActionNames, PathCopy)

            if temp[1] not in ClosedList:
                # Insert at the 0th index of Open List
                OpenList.insert(0, temp)

        
        # Sorting through the list so that the value with the least f(n) is at the 0th Index
        InsertionSort(OpenList)
        # Node at 0th index (If this Node is equal to the goal node the loop will end and the path is complete)
        Node = OpenList[0][1]
        # The List of actions through which the goal node is achived
        Actions = OpenList[0][2]
        # The Path that has been taken
        Path = OpenList[0][3] 

        del OpenList[0]

    Path.append(Node)
    # print(Path)
    return Path


a = JumpingFrogs()
b = RoutePlanning("Islamabad", "Hunza", "/Users/fatimaalvi/Desktop/Assignment01/Code/cities.csv", "/Users/fatimaalvi/Desktop/Assignment01/Code/Connections.csv", "/Users/fatimaalvi/Desktop/Assignment01/Code/heuristics.csv")
print(aStarSearch(a))
print(aStarSearch(b))
