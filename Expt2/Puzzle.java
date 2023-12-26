import java.util.Stack;
import java.util.List;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.HashSet;
import java.util.Set;
import java.util.Arrays;

class Node implements Comparable<Node> {
    int[][] state;
    int depth;
    int misplacedTiles;
    int totalCost;
    Node parent;

    public Node(int[][] state, int depth, int misplacedTiles, Node parent) {
        this.state = state;
        this.depth = depth;
        this.misplacedTiles = misplacedTiles;
        this.parent = parent;
        this.totalCost = depth + misplacedTiles;
    }

    @Override
    public int compareTo(Node other) {
        return Integer.compare(this.totalCost, other.totalCost);
    }
}

public class Puzzle {
    private static List<Node> getNeighbors(Node currentNode, int[][] finalState) {
        List<Node> neighbors = new ArrayList<Node>();
        int[] dx = {-1, 1, 0, 0};
        int[] dy = {0, 0, -1, 1};

        for (int i = 0; i < 4; i++) {
            int newX = -1, newY = -1;
            for (int j = 0; j < currentNode.state.length; j++) {
                for (int k = 0; k < currentNode.state[j].length; k++) {
                    if (currentNode.state[j][k] == 0) {
                        newX = j + dx[i];
                        newY = k + dy[i];
                        break;
                    }
                }
            }

            if (isValidMove(newX, newY, currentNode.state.length, currentNode.state[0].length)) {
                int[][] newState = copyState(currentNode.state);
                swap(newState, newX, newY, currentNode.state);
                Node neighbor = new Node(newState, currentNode.depth + 1, countMisplacedTiles(newState, finalState), currentNode);
                neighbors.add(neighbor);
            }
        }

        return neighbors;
    }

    private static boolean isValidMove(int x, int y, int numRows, int numCols) {
        return (x >= 0 && x < numRows && y >= 0 && y < numCols);
    }

    private static int[][] copyState(int[][] state) {
        int[][] newState = new int[state.length][];
        for (int i = 0; i < state.length; i++) {
            newState[i] = Arrays.copyOf(state[i], state[i].length);
        }
        return newState;
    }

    private static void swap(int[][] state, int x, int y, int[][] currentState) {
        int temp = state[x][y];
        state[x][y] = 0;
        for (int i = 0; i < currentState.length; i++) {
            for (int j = 0; j < currentState[i].length; j++) {
                if (currentState[i][j] == 0) {
                    state[i][j] = temp;
                    return;
                }
            }
        }
    }

    private static void printState(int[][] state) {
        for (int i = 0; i < state.length; i++) {
            for (int j = 0; j < state[i].length; j++) {
                System.out.print(state[i][j] + " ");
            }
            System.out.println();
        }
    }

    private static void printSolution(Node goalNode) {
        Stack<Node> path = new Stack<Node>();
        Node currentNode = goalNode;
        while (currentNode != null) {
            path.push(currentNode);
            currentNode = currentNode.parent;
        }

        int step = 0;
        while (!path.isEmpty()) {
            currentNode = path.pop();
            System.out.println("Step " + step++ + ":");
            printState(currentNode.state);
            System.out.println();
        }
    }

    private static int countMisplacedTiles(int[][] state, int[][] finalState) {
        int count = 0;
        for (int i = 0; i < state.length; i++) {
            for (int j = 0; j < state[i].length; j++) {
                if (state[i][j] != 0 && state[i][j] != finalState[i][j]) {
                    count++;
                }
            }
        }
        return count;
    }

    public static void solvePuzzle(int[][] initialState, int[][] finalState) {
        PriorityQueue <Node> openSet = new PriorityQueue <Node>();
        Set <String> closedSet = new HashSet <String>();

        Node initialNode = new Node(initialState, 0, countMisplacedTiles(initialState, finalState), null);
        openSet.add(initialNode);

        while (!openSet.isEmpty()) {
            Node currentNode = openSet.poll();
            closedSet.add(Arrays.deepToString(currentNode.state));

            if (Arrays.deepEquals(currentNode.state, finalState)) {
                printSolution(currentNode);
                return;
            }

            List<Node> neighbors = getNeighbors(currentNode, finalState);
            for (Node neighbor : neighbors) {
                if (!closedSet.contains(Arrays.deepToString(neighbor.state))) {
                    openSet.add(neighbor);
                }
            }
        }

        System.out.println("No solution found!");
    }

    public static void main(String[] args) {
        int[][] initialState = {
                {2, 8, 3},
                {1, 6, 4},
                {7, 0, 5}
        };

        int[][] finalState = {
                {1, 2, 3},
                {8, 0, 4},
                {7, 6, 5}
        };

        solvePuzzle(initialState, finalState);
    }
}
