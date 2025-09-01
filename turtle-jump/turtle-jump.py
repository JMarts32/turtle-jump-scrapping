def turtlteJump(path: list) -> int:
    total_rocks = len(path)
    
    # Base case 1
    if total_rocks < 2:
        return 0
    
    jump_cost = 0
    
    for current_rock in range(total_rocks - 2):
        jump_cost = max(jump_cost, path[current_rock + 2] - path[current_rock])
        
    return jump_cost