import random
import Splits

while True:
    command = input("\nEnter command: ").lower()

    if command == "new":
        print()
        try:
            target = input("Target: ")
            target = int(target)
            part_count = int(input("Number of parts: "))
        except:
            if target.lower() == "random":
                target = random.randint(24, 100)
                part_count = random.randint(3, 5)
            else:
                print("\nInvalid input.")
                continue
        print()
        puzzle = Splits.Puzzle(target, part_count)
        puzzle.generate_puzzle()
        puzzle.display_puzzle()

        solver = Splits.Solver(puzzle)
        solver.solve()
        
    elif command == "solution":
        print()
        try:
            puzzle.display_solution()
        except:
            print("Generate puzzle first.")
        
    else:
        print("\nCommand not recognized.")
            


