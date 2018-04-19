import random

class Node(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.color = None
    
    def set_color(self, color):
        self.color = color

class Subset(object):
    
    random_nodes_values = []
    registred_node = []

    def __init__(self, name, list_of_nodes):
        self.nodes = []
        self.name  = list_of_nodes[0]
        self.count = len(list_of_nodes)-1
        for element in list_of_nodes:
            node = self.is_already_node(element)
            if len(node) == 0 :
                n = Node(element, self.generate_random_node_value())
            else:
                n = node[0]
            self.registred_node.append(n)
            self.nodes.append(n)

    def generate_random_node_value(self):
        range_values = range(1, 99)
        valid_list = list(set(range_values) - set(self.random_nodes_values))
        if len(valid_list) > 0:
            value = random.choice(valid_list)
        else:
            return False
        self.random_nodes_values.append(value)
        return value

    def node_with_max_value(self):
        sorted_list = sorted(self.nodes, key=lambda x: x.value, reverse=True)
        if len(sorted_list) > 0:
            return sorted_list[0]
        
    def node_with_min_value(self):
        sorted_list = sorted(self.nodes, key=lambda x: x.value, reverse=False)
        if len(sorted_list) > 0:
            return sorted_list[0]
    
    def is_already_node(self, name):
        return [node for node in self.registred_node if node.name == name]
    

class Graph(object):
    colors = ['RED', 'BLUE', 'GREEN', 'YELLOW', 'PINK', 'ORANGE']
    nodes = []
    node_to_remove = []
    def __init__(self, source):
        self.sets = []
        self.count = 0
        with open(source) as s:
            for line in s:
                self.count = self.count + 1 
                l = line.split(';')
                nodes = [item.rstrip('\n') for item in l]
                sub_set = Subset(nodes[0], nodes)
                self.sets.append(sub_set)

    def solve(self):
        i = 0         
        while len(self.nodes) < self.count : 
            for subset in self.sets:
                node_max = subset.node_with_max_value()
                #if isinstance(node_max, Node) == False:
                #    continue;  
                #else:
                if node_max.name == subset.nodes[0].name:
                    node_max.set_color(self.colors[i])
                    if node_max not in self.nodes:
                        self.nodes.append(node_max)
                        self.node_to_remove.append(node_max)
            self.color_non_adjacent_nodes_left(self.colors[i])
            self.clear_graph()
            i = i + 1
        self.number_of_color_used = i
        self.output_result()

    def color_non_adjacent_nodes_left(self, color):
        for subset in self.sets[:]:
            indice = False            
            for node in subset.nodes:
                if node.color != None:
                    indice = True
            if indice == False:
                subset.nodes[0].set_color(color)
                self.nodes.append(subset.nodes[0])
                self.node_to_remove.append(subset.nodes[0])

    def remove_node_from_all_subsets(self, _node):
        for subset in self.sets[:]:
            for node in subset.nodes:
                if node.name == _node.name:
                    subset.nodes.remove(_node)
    
    def clear_graph(self):
        for n in self.node_to_remove[:]:
            for subset in self.sets:
                if subset.name == n.name:
                    self.sets.remove(subset)
            self.remove_node_from_all_subsets(n)
    
    def output_result(self):
        for n in self.nodes:
            print "[{}]  {}".format(n.color, n.name)

        print "\nNodes colored :{}\nNumber of color used : {}".format(str(len(self.nodes)), self.number_of_color_used)

if __name__ == '__main__':
    graph = Graph('regions_france.txt')
    graph.solve()
