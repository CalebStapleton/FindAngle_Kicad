import pcbnew
import math

def find_90_v10():
    board = pcbnew.GetBoard()
    points = {}
    
    print("Scanning layout tracks...")
    
    # Safely extract tracks using modern instance tracking
    # (Accounts for the internal API transition)
    all_tracks = [t for t in board.GetTracks() if isinstance(t, pcbnew.PCB_TRACK)]
    
    for track in all_tracks:
        # Get start/end positions as native Vector objects or tuples
        start_pos = track.GetStart()
        end_pos = track.GetEnd()
        
        start = (start_pos.x, start_pos.y)
        end = (end_pos.x, end_pos.y)
        
        # Calculate angle of the segment (0 to 180 deg)
        # Using math.atan2(dy, dx)
        dy = end[1] - start[1]
        dx = end[0] - start[0]
        
        angle = round(math.degrees(math.atan2(dy, dx)) % 180, 1)
        
        # Map angles meeting at specific coordinates
        for pt in (start, end):
            points.setdefault(pt, []).append(angle)
                
    found = False
    for pt, angles in points.items():
        # A junction requires at least two distinct traces joining
        if len(angles) >= 2:
            # Evaluate all unique intersecting pairs at this specific node
            for i in range(len(angles)):
                for j in range(i + 1, len(angles)):
                    diff = abs(angles[i] - angles[j])
                    
                    # Target explicit 90° intersections allowing a tiny margin
                    if 87.0 <= diff <= 93.0:
                        # Use internal unit conversion helper for reliability
                        mm_x = pcbnew.ToMM(pt[0])
                        mm_y = pcbnew.ToMM(pt[1])
                        
                        print(f"🎯 90° Junction found at X: {mm_x:.3f} mm, Y: {mm_y:.3f} mm")
                        found = True
                        
    if not found:
        print("No separate 90° track intersections detected.")
        print("If you drew it as one continuous segment, try breaking it into two pieces to test!")

# Run it
#find_90_v10()
