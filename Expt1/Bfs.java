package Expt1;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class Bfs {
    private static void bfs(int[][] matrix, int n, int src, int dst) {
        Queue<Integer> queue = new LinkedList<Integer>();
        boolean[] visited = new boolean[n];
        Arrays.fill(visited, false);

        queue.add(src);
        visited[src] = true;

        while (!queue.isEmpty()) {
            int current = queue.poll();
            System.out.print(current + " ");

            if (current == dst) {
                System.out.println("\nDestination found!");
                return;
            }

            for (int i = 0; i < n; i++) {
                if (matrix[current][i] == 1 && !visited[i]) {
                    queue.add(i);
                    visited[i] = true;
                }
            }
        }

        System.out.println("\nDestination not reachable from the source.");
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        int n = getValidInput("Enter the number of elements: ", 1, Integer.MAX_VALUE);

        int[][] matrix = new int[n][n];

        populateMatrix(matrix, n);

        int src = getValidInput("\nEnter the source node: ", 0, n - 1);
        int dst = getValidInput("Enter the destination node: ", 0, n - 1);

        bfs(matrix, n, src, dst);

        // Close the Scanner in the main method after using it
        input.close();
    }

    private static int getValidInput(String prompt, int min, int max) {
        Scanner input = new Scanner(System.in);
        int value = -1;

        while (value < min || value > max) {
            System.out.print(prompt);
            value = input.nextInt();
            if (value < min || value > max) {
                System.out.println("Invalid input. Try again.");
            }
        }
        return value;
    }

    private static void populateMatrix(int[][] matrix, int n) {
        int n1 = 0, n2 = 0;
        Scanner input = new Scanner(System.in);

        while (true) {
            System.out.print("\nEnter the x - vertex (Enter -1 to break): ");
            n1 = input.nextInt();

            if (n1 == -1) {
                break;
            }

            System.out.print("Enter the y - vertex: ");
            n2 = input.nextInt();

            if (isValidVertex(n1, n2, n)) {
                matrix[n1][n2] = 1;
                matrix[n2][n1] = 1;
            } else {
                System.out.println("Invalid vertices. Try again.");
            }
        }
    }

    private static boolean isValidVertex(int n1, int n2, int n) {
        return n1 >= 0 && n1 < n && n2 >= 0 && n2 < n;
    }
}
