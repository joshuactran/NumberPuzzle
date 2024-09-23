import Splits

while True:
    command = input("\nEnter command: ").lower()

    if command == "new":
        print()
        try:
            target = int(input("Target: "))
            part_count = int(input("Number of parts: "))
        except:
            print("Invalid input.")
            continue
        print()
        puzzle = Splits.Puzzle(target, part_count)
        puzzle.generate_puzzle()
        puzzle.display_puzzle()
        
    elif command == "solution":
        print()
        try:
            puzzle.display_solution()
        except:
            print("Generate puzzle first.")

    elif command == "solve":
        solver = Splits.Solver(puzzle)
        solver.solve()
        
    else:
        print("\nCommand not recognized.")
            


