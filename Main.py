import random
from SolveMaze import SolveMaze
from Maze import Maze


class Main:
    def __init__(self, size):
        self.agent_maze = Maze().generate_blank_maze(size)
        self.actual_maze = Maze().generate_actual_maze(size)
        self.size = size
        self.solvedMaze = []
        self.start_node = None
        self.goal_node = None

    def generate_random_start_and_goal_nodes(self):
        while True:
            start_node_actual = self.actual_maze[random.randint(0, self.size-1)][random.randint(0, self.size-1)]
            goal_node_actual = self.actual_maze[random.randint(0, self.size-1)][random.randint(0, self.size-1)]
            if (start_node_actual.cost == 1) & (goal_node_actual.cost == 1) & (start_node_actual != goal_node_actual):
                break
        self.start_node = self.agent_maze[start_node_actual.x][start_node_actual.y]
        self.goal_node = self.agent_maze[goal_node_actual.x][goal_node_actual.y]
        return start_node_actual, goal_node_actual

    def traverse_path(self, goal_node, start_node):
        path = [goal_node]
        currentNode = goal_node
        while currentNode is not start_node:
            currentNode = currentNode.parent
            path.append(currentNode)
        return path

    def bolckage_status_of_children(self, start_node, start_node_actual):
        if start_node_actual.right_child is not None:
            start_node.right_child.cost = start_node_actual.right_child.cost
        if start_node_actual.left_child is not None:
            start_node.left_child.cost = start_node_actual.left_child.cost
        if start_node_actual.top_child is not None:
            start_node.top_child.cost = start_node_actual.top_child.cost
        if start_node_actual.down_child is not None:
            start_node.down_child.cost = start_node_actual.down_child.cost

    def repeated_forward(self, start_node_actual, goal_node_actual):
        counter = 0
        start_node = self.start_node
        self.bolckage_status_of_children(start_node, start_node_actual)
        while start_node is not self.goal_node:
            counter += 1
            start_node.update_g(0)
            start_node.update_h(self.goal_node)
            start_node.update_search(counter)
            self.goal_node.update_g(float("inf"))
            self.goal_node.update_search(counter)
            if SolveMaze().forward_A_star(start_node, self.goal_node, self.agent_maze) == "I can't reach the target":
                print("I can't reach the target")
                return
            path = self.traverse_path(self.goal_node, start_node)
            path.reverse()
            for i in path:
                if i.cost == self.actual_maze[i.x][i.y].cost:
                    if i in self.solvedMaze:
                        if i is self.start_node:
                            continue
                        self.solvedMaze.pop(self.solvedMaze.index(i))
                        continue
                    self.solvedMaze.append(i)
                else:
                    start_node = self.solvedMaze.pop()
                    start_node_actual = self.actual_maze[start_node.x][start_node.y]
                    self.bolckage_status_of_children(start_node, start_node_actual)
                    break
            if self.solvedMaze[len(self.solvedMaze)-1] == self.goal_node:

                print("I reached the goal: ")
                for a in self.solvedMaze:
                    a.print()
                return

    def main(self):
        start_node_actual, goal_node_actual = self.generate_random_start_and_goal_nodes()
        print(start_node_actual.x, start_node_actual.y, goal_node_actual.x, goal_node_actual.y)
        self.repeated_forward(start_node_actual, goal_node_actual)


for k in range(10):
    Main(101).main()
