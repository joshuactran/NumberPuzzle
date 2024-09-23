import random
import math
import re

# Return a list of two numbers that add up to num
def split_add(num):
    rng = random.randint(1, num - 1)
    return [rng, num - rng]

# Return a list of two numbers (a, b) such that b - a = num
def split_sub(num):
    rng = random.randint(1, num)
    return [rng, num + rng]

# Return a list of factors of num
def factorize(num):
    ans = []
    for i in range(1, int(math.sqrt(num)) + 1):
        if num % i == 0:
            ans.append(i)
            ans.append(num // i)
    return ans

# Return a list of two numbers that multiply up to num            
def split_mult(num, factors):
    rng = random.choice(factors)
    return [rng, num // rng]

# Return a list of two numbers (a, b) such that b/a = num
def split_div(num):
    rng = random.choice([2, 3, 4])
    return [rng, num * rng]

class Puzzle:
    def __init__(self, target, part_count):
        self.target = target
        self.part_count = part_count

    # Split target into the specified number of parts using random operations
    def generate_puzzle(self):
        # Reset the parts and solution
        self.parts = [self.target]
        self.solution = []
        standard_dist = ["+", "-", "*", "/"]
        prime_dist = ["+", "-", "/"]

        # Need to perform (n - 1) split operations to have n parts
        for i in range(self.part_count - 1):
            # Choose a random part (that isn't 1) to split
            while True:
                num = random.choice(self.parts)
                if num != 1:
                    break
                
            # Factorize the chosen part, then choose from a split operation distribution depending on primality
            # split_mult(p) will always give a 1, so we should choose it less often
            factors = factorize(num)
            if len(factors) == 2:
                operation = random.choice(prime_dist)
            else:
                operation = random.choice(standard_dist)

            # Perform the chosen operation on the chosen part and update self.parts
            if operation == "+":
                splits = split_add(num)
                self.parts.pop(self.parts.index(num))
                self.parts += splits
            elif operation == "-":
                splits = split_sub(num)
                self.parts.pop(self.parts.index(num))
                self.parts += splits
            elif operation == "*":
                # Remove 1 and the number from factors
                corrected_factors = [factor for factor in factors if (factor != 1 and factor != num)]
                splits = split_mult(num, corrected_factors)
                self.parts.pop(self.parts.index(num))
                self.parts += splits
            elif operation == "/":
                splits = split_div(num)
                self.parts.pop(self.parts.index(num))
                self.parts += splits

            # Add split step to self.solution
            solution_step = f"{splits[1]} {operation} {splits[0]} = {num}"
            self.solution.append(solution_step)

        self.solution.reverse()
        random.shuffle(self.parts)

    # Print the final list of parts and the target
    def display_puzzle(self):
        print(f"Get to {self.target} from {self.parts}")

    # Print the solution steps
    def display_solution(self):
        for step in self.solution:
            print(step)       

class Solver:
    # Inherit the target and parts from a Puzzle object
    def __init__(self, puzzle):
        self.target = puzzle.target
        self.parts = puzzle.parts
        self.current_parts = puzzle.parts.copy()

    # Enter solving mode
    def solve(self):
        step_pattern = "[0-9]+ [\+\-\*\/] [0-9]+"

        while True:
            command = input("\nEnter solve command: ").lower()

            # Start over from the original parts
            if command == "reset":
                self.current_parts = self.parts.copy()

            elif command == "remind":
                print()
                print(self.current_parts, f"--> {self.target}")

            # Command is of the form number operator number (1 + 1)
            elif re.fullmatch(step_pattern, command):
                components = command.split()
                num1 = int(components[0])
                num2 = int(components[2])
                operator = components[1]

                # Both numbers should be in current_parts
                # If num1 and num2 are the same, there must be at least 2 copies of it in current_parts
                if num1 not in self.current_parts or num2 not in self.current_parts or (num1 == num2 and self.current_parts.count(num1) < 2):
                    print("\nOnly select numbers from the available parts")
                    continue

                else:
                    # Calculate new number if it's legal
                    if operator == "+":
                        new = num1 + num2
                    elif operator == "-":
                        new = num1 - num2
                        if new < 1:
                            print("\nNumbers cannot be negative")
                            continue
                    elif operator == "*":
                        new = num1 * num2
                    elif operator == "/":
                        if num1 % num2 == 0:
                            new = num1 // num2
                        else:
                            print("\nNumbers must be integers")
                            continue

                    # Pop the old parts and append the new number
                    self.current_parts.pop(self.current_parts.index(num1))
                    self.current_parts.pop(self.current_parts.index(num2))
                    self.current_parts.append(new)
                    print(command, f" = {new}")
                    print(self.current_parts, f"--> {self.target}")

                    if len(self.current_parts) == 1:
                        if self.current_parts[0] == self.target:
                            print("\nYou win!")
                            return
                        else:
                            print("\nWrong number. Try again.")
                            self.current_parts = self.parts.copy()
                            print()
                            print(self.current_parts, f"--> {self.target}")

            elif command == "quit":
                return

            else:
                print("\nCommand not recognized")
