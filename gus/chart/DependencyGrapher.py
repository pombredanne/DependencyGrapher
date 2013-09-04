import pydot
            
class DependencyGrapher:
    '''
    Creates a visualization of the team dependency graph
    '''
    def __get_status_color__(self, status):
        status_color = {
                        'New':'red',
                        'Never':'red',
                        'Deferred':'red',
                        'Fixed':'yellow',
                        'Committed':'yellow',
                        'QA In Progress':'yellow',
                        'Completed':'green',
                        'Closed':'green',
                        }
        if status in status_color.keys():
            color = status_color[status]
        else:
            color = 'orange'
            
        return color
    
    def __get_line_style__(self, status):
        line_style = {
                      'Never':'dotted',
                      }
        
        if status in line_style.keys():
            style = line_style[status]
        else:
            style = 'filled'
            
        return style
        
    
    def __work_node__(self, workid, worklabel, status, subject,rank):
        label = "%s (%s)\nRank[%s]\n%s" % (worklabel,status,rank,subject)
            
        node = pydot.Node(self.__slice_label__(label))
        node.set_URL(self.__gus_url__(workid))
        node.set_style(self.__get_line_style__(status))
        node.set_fillcolor(self.__get_status_color__(status))
        return node
    
    def __my_work_node__(self, dep):
        return self.__work_node__(dep.my_work().id, dep.my_work().name(), dep.my_work().status(), dep.my_work().label(),dep.my_work().rank())
    
    def __their_work_node__(self, dep):
        return self.__work_node__(dep.their_work().id, dep.their_work().name(), dep.their_work().status(), dep.their_work().label(), dep.their_work().rank())
    
    def __subgraph__(self, graph, label):
        name = 'cluster_%s' % label.replace(' ', '_')
        subgraph = pydot.Subgraph(name)
        subgraph.set_label(label)
        graph.add_subgraph(subgraph)
            
        return subgraph
    
    def __slice_label__(self, label):
        label = str(label).replace(":", " ")
        words = label.split(' ')
        out = []
        max_length = 8
        count = 0
        for word in words:
            out.append(word)
            count = count + 1
            if count >= max_length:
                out.append("\n")
                count = 0
        return " ".join(out)
    
    def __gus_url__(self, ident):
        return "https://gus.my.salesforce.com/%s" % ident
    
    def __add_node__(self, graph, dep):
        label = dep.deliverable()
        dep_node = pydot.Node('%s (%s)\n%s\n%s' % (dep.name(), dep.status(), self.__slice_label__(label), dep.target()))
        dep_node.set_URL(self.__gus_url__(dep.id))
        dep_node.set_shape('rectangle')
        dep_node.set_style(self.__get_line_style__(dep.status()))
        dep_node.set_fillcolor(self.__get_status_color__(dep.status()))
        graph.add_node(dep_node)
        
        if dep.my_work() is not None:
            work = self.__my_work_node__(dep)
            team_subgraph = self.__subgraph__(graph, dep.my_work().team())
            if dep.my_work().sprint() is not None:
                subgraph = self.__subgraph__(team_subgraph, dep.my_work().sprint())
                team_subgraph.add_subgraph(subgraph)
            else:
                subgraph = team_subgraph
                
            subgraph.add_node(work)
            graph.add_edge(pydot.Edge(work, dep_node))
        
        if dep.their_work() is not None:
            work = self.__their_work_node__(dep)
            team_subgraph = self.__subgraph__(graph, dep.their_work().team())
            if dep.their_work().sprint() is not None:
                subgraph = self.__subgraph__(team_subgraph, dep.their_work().sprint())
                team_subgraph.add_subgraph(subgraph)
            else:
                subgraph = team_subgraph
                
            subgraph.add_node(work)
            edge = pydot.Edge(dep_node, work)
            edge.set_style(self.__get_line_style__(dep.their_work().status()))
            graph.add_edge(edge)
            
        for parent in dep.parents():
            self.__add_node__(graph, parent)
            
        for child in dep.children():
            self.__add_node__(graph, child)

    def __plot_graph__(self, data, label):
        '''
        Creates a graph visualization using the label as a filename and the graph data from the client
        '''
        graph = pydot.Dot(graph_type='digraph', graph_name='deps', label=label, rankdir='LR', strict='strict', splines='ortho')
        for dep in data:
            self.__add_node__(graph, dep)
        
        return graph
    
    def __make_web__(self, label):
        with open("%s.map" % label, 'r') as m:
            map_data = m.read()
            m.close()
            
        with open("%s.html" % label, 'w') as html:
            html.write("<html><head><title>%s</title></head>\n" % label)
            html.write("<body><img src='%s.png' usemap='#deps' />" % label)
            html.write(map_data)
            html.write("</body></html>")
            html.close()
        
    def graph_dependencies(self, data, label):
        graph = self.__plot_graph__(data, label)
        label = label.replace('[&/\]','_')
        with open('%s.dot' % label, 'w') as f:
            f.write(graph.to_string())    
            f.close()
        
        graph.write('%s.pdf' % label, format='pdf')
        graph.write('%s.png' % label, format='png')
        graph.write('%s.map' % label, format='cmapx')
        self.__make_web__(label)
        
