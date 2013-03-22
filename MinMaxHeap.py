import math

'''An implementation of the MIN-MAX Datastructure as 
described in the following paper:
http://www.cs.otago.ac.nz/staffpriv/mike/Papers/MinMaxHeaps/MinMaxHeaps.pdf
'''
class MinMaxHeap(object):

	def __init__(self):
		self.root=None
		self.size=0
		self.lastInserted=None

	def set_root(self, node):
		self.root = node

	def get_depth(self):
		if self.size > 0:
			return math.floor(math.log(self.size, 2));
		return 0

	def get_insert_depth(self):
		if self.size > 0:
			return math.floor(math.log(self.size + 1, 2)) - 1;
		return 0

	def get_current_depth(self, index):
		if(index >= 0):
			return math.floor(math.log(index+1, 2));
		return 0

	def isMinLevel(self, index):
		return (self.get_current_depth(index) % 2) == 0

	def find_position(self):
		#get the depth right before the leaf level
		return self._find_position(self.root, self.get_insert_depth())

	def _find_position(self, node, depth):
		#get the current depth we are at based on our index
		current_depth = self.get_current_depth(node.get_index())
		#continue traversing until we hit this depth
		if current_depth < depth:
			for child in node.get_children():
				ret = self._find_position(child, depth)
				if(ret != False):
					return ret
		#once we hit the depth
		elif current_depth == depth:
			#check if node is not full
			if node.get_num_children() < 2:
				return node
		
		return False

	def get_last_element(self):
		if self.root:
			return self._get_last_element(self.root, self.get_depth())
		return None

	def _get_last_element(self, node, depth):
		current_depth = self.get_current_depth(node.get_index())

		if current_depth < depth:
			for child in node.get_children():
				ret = self._get_last_element(child, depth)
				if ret != False:
					return ret
		elif current_depth == depth:
			if node.get_index() == self.size-1:
				return node
		return False


	def find_min_replacement(self, node):
		elements = []
		smallest = None
		for child in node.get_children():
			elements.append(child)
			elements += child.get_children()

		for child in elements:
			if smallest == None:
				smallest = child
				continue
			elif child.get_value() < smallest.get_value():
				smallest = child

		return smallest

	def find_max_replacement(self, node):
		elements = []
		largest = None
		for child in node.get_children():
			elements.append(child)
			elements += child.get_children()

		for child in elements:
			if largest == None:
				largest = child
				continue
			elif child.get_value() > largest.get_value():
				largest = child

		return largest


	def insert(self, value):
		#create the new element
		new = Node(self.size, value);

		#first insert check
		if self.size <= 0: 
			self.root = new
			self.size += 1
			return

		#find the available node to insert into
		node = self.find_position()

		#update the size
		self.size += 1
		#add the element
		node.add_child(new)

		#if we are on a min level
		if self.isMinLevel(new.get_index()):
			parent = new.get_parent()
			if new.has_parent() and new.get_value() > parent.get_value():
				self.swap(new, parent)
				self.bubble_up_max(parent)
			else:
				self.bubble_up_min(new)

		else:
			parent = new.get_parent()
			if new.has_parent() and new.get_value() < parent.get_value():
				self.swap(new, parent)
				self.bubble_up_min(parent)
			else:
				self.bubble_up_max(new)

	def extract_min(self):
		if self.root:
			minVal = self.root.get_value()

			if self.root.has_children():
				replacement = self.get_last_element()
				self.root.set_value(replacement.get_value())
				replacement.get_parent().remove_child(replacement)
				self.size-=1
				self.trickle_down_min(self.root)
			else:
				self.root = None
				self.size-=1

			return minVal
		return None

	def extract_max(self):
		if self.root:
			if self.root.has_children():
				maxNode = self.root.get_max_child()
				maxVal = maxNode.get_value()
				rep = self.get_last_element()
				maxNode.set_value(rep.get_value())
				rep.get_parent().remove_child(rep)
				self.size-=1
				self.trickle_down_max(maxNode)
				return maxVal
			else:
				maxVal = self.root.get_value()
				self.root = None
				self.size-=1
				return maxVal
		else:
			return None

	def swap(self, lowerNode, higherNode):
		#literally just swap the values
		lowerVal = lowerNode.get_value()
		lowerNode.set_value(higherNode.get_value())
		higherNode.set_value(lowerVal)

	def bubble_up_min(self, node):
		if node.has_grandparent():
			grandpa = node.get_grandparent()
			if node.get_value() < grandpa.get_value():
				self.swap(node, grandpa)
				self.bubble_up_min(grandpa)

	def bubble_up_max(self, node):
		if node.has_grandparent():
			grandpa = node.get_grandparent()
			if node.get_value() > grandpa.get_value():
				self.swap(node, grandpa)
				self.bubble_up_max(grandpa)

	def trickle_down_min(self, node):

		if node.has_children():
			m = self.find_min_replacement(node)

			if m.is_grandchild_of(node):
				if m.get_value() < node.get_value():
					self.swap(m, node)
					if m.get_value() > m.get_parent().get_value():
						swap(m, m.get_parent())
					self.trickle_down_min(m)
			else: 
				if m.get_value() < node.get_value():
					self.swap(m, node)

	def trickle_down_max(self, node):

		if node.has_children():
			m = self.find_max_replacement(node)

			if m.is_grandchild_of(node):
				if m.get_value() > node.get_value():
					self.swap(m, node)
					if m.get_value() < m.get_parent().get_value():
						swap(m, m.get_parent())
					self.trickle_down_max(m)
			else: 
				if m.get_value() > node.get_value():
					self.swap(m, node)

	def __str__(self):
		'''Perform a breadth first search for each depth therefore 
		the heap would be printed row by row starting from the root'''
		s = ''
		if self.root:
			Q = [self.root]
			while(len(Q) > 0):
				item = Q.pop(0)
				s += str(item.get_value()) + ','
				Q += item.get_children()

			s = '[' + s[:-1] + ']'
		return s


'''A Data structure representing a Node element 
in the MIN-MAX Heap. It is augmented to know its parent
and its index along with its value.'''
class Node(object):

	def __init__(self, index, value, parent=None):
		self.value=value
		self.index=index
		self.parent=parent
		self.children = []

	def set_value(self, newVal):
		self.value = newVal

	def get_value(self):
		return self.value

	def get_index(self):
		return self.index

	def set_parent(self, pnode):
		self.parent = pnode

	def get_parent_index(self):
		return self.parent.get_index()

	def get_parent(self):
		return self.parent

	def get_grandparent(self):
		if self.has_grandparent():
			return self.parent.get_parent()
		return None

	def get_children(self):
		return self.children

	def get_max_child(self):
		largest = None
		for child in self.get_children():
			if largest == None:
				largest = child
				continue
			elif child.get_value() > largest.get_value():
				largest = child
		return largest

	def add_child(self, node):
		if(len(self.children) < 2):
			self.children.append(node);
			node.set_parent(self)
			return True
		return False

	def remove_child(self, node):
		for child in self.children:
			if child.get_value() == node.get_value():
				self.children.remove(child)
				return True
		return False

	def has_grandparent(self):
		if self.parent != None and self.parent.has_parent():
			return True
		return False

	def has_children(self):
		return len(self.children) > 0

	def get_num_children(self):
		return len(self.children)

	def has_parent(self):
		return self.parent != None

	def is_grandchild_of(self, node):
		return self.get_grandparent() == node

	def __str__(self):
		return str(self.value)

if __name__ == "__main__":

	heap = MinMaxHeap()
	heap.insert(1)
	heap.insert(90)
	heap.insert(100)
	heap.insert(4)
	heap.insert(8)
	heap.insert(3)
	heap.insert(2)
	heap.insert(85)
	heap.insert(40)
	heap.insert(55)
	heap.insert(70)
	heap.insert(75)
	heap.insert(60)
	heap.insert(50)
	heap.insert(10)
	heap.insert(80)
	
	'''Extract Min Test'''
	print('>>Extract Min Test')
	for i in range(heap.size):
		print(heap)
		print(heap.extract_min())
		print(heap)
		print('-'*30)
	
	heap.insert(1)
	heap.insert(90)
	heap.insert(100)
	heap.insert(4)
	heap.insert(8)
	heap.insert(3)
	heap.insert(2)
	heap.insert(85)
	heap.insert(40)
	heap.insert(55)
	heap.insert(70)
	heap.insert(75)
	heap.insert(60)
	heap.insert(50)
	heap.insert(10)
	heap.insert(80)

	'''Extract Max Test'''
	print('>>Extract Max Test')
	for i in range(heap.size):
		print(heap)
		print(heap.extract_max())
		print(heap)
		print('-'*30)
	






