class Machine:
	#constructor, takes only text and instantiates all variables
	def __init__(self, text):
		self.type = text
		self.headerText = ''
		self.footerText = ''
		self.edgeList = []
		self.stateList = []

	#creates state objects		
	def state(self, state_name, action_string, edge_list= None):
		
		#create new state and append to list	
		newState = State(state_name,action_string,edge_list)
		self.stateList.append(newState)
	
	#loops through input list and creates edge objects
	def edges( self, *args_list):
		tempEdgeList = []
		for arg in args_list:
			if len(arg) < 3:
				newEdge = edge(arg[0],arg[1],None)
				tempEdgeList.append(newEdge)
			else:
				newEdge = edge(arg[0],arg[1],arg[2])
				tempEdgeList.append(newEdge)
		return tempEdgeList
			
	#creates edge objects		
	def edge(self, event_name, next_state, optional_action_string = ""):
		
		
		#calls edge class and appends to list
		newEdge = Edge(event_name, next_state, optional_action_string)
		self.edgeList.append(newEdge)

		return newEdge
	#takes footer input and stores in variable
	def footer(self, text):
		self.footerText = text

	#takes header input and stores in variable
	def header(self, text):
		self.headerText = text
	
	#generate c++ code
	def gen(self):
		
		#print header
		print self.headerText

		print"""
#include <iostream>
using namespace std;

enum State { 	"""
		#loop through state to get state names and print
		for state in self.stateList:
			print state.state + "_STATE," 
		print """};

enum Event {"""
		#loop through edges to get event names
		for e in self.edgeList:
			print e.event + "_EVENT,"
		print """INVALID_EVENT
};

const char * EVENT_NAMES[] = {"""
		#loop through edges to get event names
		for a in self.edgeList:
			print "\"" +  a.event  +"\","
		print """};

Event get_next_event();

Event string_to_event(string event_string) {"""
		#loop through edges to get even names
		for b in self.edgeList:
			print "if (event_string == \"" + b.event + "\") {return " + b.event + "_EVENT;}"
		print """return INVALID_EVENT;
}
"""
		#print machine name
		print "int "  + self.type + """(State intial_state) {
	State state = initial_state;
	Event event;
	while(true) {
		switch(state) {"""		
		#loop through states		
		for s in self.stateList:
			
			print "			case " + s.state + "_STATE:"
			print "				cerr << \"state " + s.state + "\" << endl;"
			print s.action
			print """
				event = get_next_event();
				cerr << "event" << EVENT_NAMES[event] << endl;
				switch (event) {
"""			
			#loop through edges and check if edges are none
			if not (s.edge is None):
				for l in s.edge:
					print "				case " +l.event + "_EVENT:"
					print l.option
					print "					state = " + l.next + "_STATE;"
					print "					break;"
			else:
				print """				default:
					cerr << "INVALID EVENT" << event << " in state END << endl;
					return -1;
				}
				break;""" 
		print"""
		}
	}
}"""	

		#print footer
		print self.footerText

#edge class
class Edge:
	
	#edge constructor
	def __init__(self, event_name, next_state, optional_action_string="" ):
		
		self.event = event_name 
		self.next = next_state
		self.option = optional_action_string
	
#state class
class State:
	#edge constructor
	def __init__(self, state_name, action_string, edge_list = ""):
		
		self.state = state_name
		self.action = action_string
		self.edge = edge_list



