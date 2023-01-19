def rearrange_boxes(current_arm_position, box_count_per_stack):
    target_box_count = sum(box_count_per_stack) // len(box_count_per_stack)
    # Initialize variable to keep track of the current arm position and the number of commands executed
    arm_position = current_arm_position
    commands = []
    for i in range(len(box_count_per_stack)):
        # Move the arm to the left or right as necessary
        if arm_position < i:
            commands.append("RIGHT")
            arm_position += 1
        elif arm_position > i:
            commands.append("LEFT")
            arm_position -= 1
        # pick up and place boxes as necessary to reach the target box count
        while box_count_per_stack[i] < target_box_count:
            commands.append("PICK")
            box_count_per_stack[i] += 1
            commands.append("PLACE")
            box_count_per_stack[i] -= 1
            # Distribute any remaining boxes to the stacks on the left
    for i in range(len(box_count_per_stack)):
        while box_count_per_stack[i] < target_box_count:
            if arm_position > 0:
                commands.append("LEFT")
                arm_position -= 1
                commands.append("PICK")
                box_count_per_stack += 1
                commands.append("RIGHT")
                arm_position += 1
    return commands


print(rearrange_boxes())
