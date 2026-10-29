import pcbnew
import math
import wx

def find_angle(userInput: int, layer: str, checkPads: bool, checkVias: bool):
    board = pcbnew.GetBoard()
    clearUser1(layer)
    points = {}

    
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

    for pt, angles in points.items():
        # A junction requires at least two distinct traces joining
        if len(angles) >= 2:
            # Evaluate all unique intersecting pairs at this specific node
            for i in range(len(angles)):
                for j in range(i + 1, len(angles)):
                    diff = abs(angles[i] - angles[j])
                    
                    # Target explicit 90° intersections allowing a tiny margin
                    if int(float(userInput))-3 <= diff <= int(float(userInput))+3:
                        # Use internal unit conversion helper for reliability
                        mm_x = pcbnew.ToMM(pt[0])
                        mm_y = pcbnew.ToMM(pt[1])

                        test_pt = pcbnew.VECTOR2I(int(pt[0]), int(pt[1]))
                        hit_pad = any(pad.HitTest(test_pt, 0) for pad in board.GetPads() if isinstance(pad, pcbnew.PAD))
                        hit_via = any(via.HitTest(test_pt, 0) for via in board.GetTracks() if isinstance(via, pcbnew.PCB_VIA))
                        
                        # Filtering logic based on checkboxes
                        is_valid = True
                        
                        if hit_pad and not checkPads:
                            is_valid = False
                        if hit_via and not checkVias:
                            is_valid = False
                            
                        if is_valid:
                            place_marker(pt, layer)


def place_marker(pt, layer: str):
    board = pcbnew.GetBoard()
    marker = pcbnew.PCB_SHAPE(board)
    marker.SetShape(pcbnew.SHAPE_T_CIRCLE)
    marker.SetCenter(pcbnew.VECTOR2I(int(pt[0]), int(pt[1])))
    marker.SetRadius(pcbnew.FromMM(1))  # Set the radius of the circle (in internal units)
    marker.SetLayer(getattr(pcbnew, layer))
    board.Add(marker)
    pcbnew.Refresh()

def clearUser1(layer: str):
    board = pcbnew.GetBoard()
    drawing_to_remove = [d for d in board.GetDrawings() if d.GetLayer() == getattr(pcbnew, layer)]
    for d in drawing_to_remove:
        board.Remove(d)
    pcbnew.Refresh()