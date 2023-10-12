def calculate_distance(coordinates):
    points = {
    (0, 1): 2,
    (0, 2): 3.8,
    (0, 3): 2.7,
    (1, 2): 2.5,
    (1, 3): 4.1,
    (2, 3): 3.9,
    }
    start_pos = None
    now_pos = None
    vidstan = 0
    revers = False

    if len(coordinates) == 1 or len(coordinates) == 0:
        return 0
    
    for i in coordinates:
        start_pos = now_pos
        now_pos = i
        
        try:
            if start_pos > now_pos:
                start_pos, now_pos = now_pos, start_pos
                revers = True
            
            if (start_pos, now_pos) in points:
                    vidstan +=  points[(start_pos, now_pos)]             
            
            while revers:
                start_pos, now_pos = now_pos, start_pos
                revers = False            
            
        except TypeError:
            start_pos = now_pos
    return vidstan   
     
    
print(calculate_distance([0, 1, 3, 2, 0, 1, 3, 2]))
print(calculate_distance([]))
print(calculate_distance([25]))