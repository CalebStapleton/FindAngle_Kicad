import pcbnew
import math
import os

class FindAngle:

    def __init__(self):
        super(FindAngle, self).__init__()

        self.frame = None

        self.name = "Find Angle"
        self.category = "Find Angle"
        self.description = "find angles between traces in the PCB"
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

        # plugin paths
        self.plugin_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.deprecation_file_path = os.path.join(self.plugin_folder, 'deprecation.null')
        self.version_file_path = os.path.join(self.plugin_folder, 'version.txt')

    def find_angle(angleInput: float, layer: str, angleTolerance: float):
        board = pcbnew.GetBoard()
        clear_layer(layer)
        points = {}

        all_tracks = [t for t in board.GetTracks() if isinstance(t, pcbnew.PCB_TRACK)]

        filtered_tracks = filter_tracks(all_tracks)
        
        for track in filtered_tracks:
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
                        
                        # Add margins to the target intersections to allow for slight deviations in the actual angles
                        if angleInput - angleTolerance <= diff <= angleInput + angleTolerance:

                            test_pt = pcbnew.VECTOR2I(int(pt[0]), int(pt[1]))                            
                                
                            valid = True
                            if (any(pad.HitTest(test_pt, 0) for pad in board.GetPads() if isinstance(pad, pcbnew.PAD))):
                                    valid = False
                            elif (any(via.HitTest(test_pt, 0) for via in board.GetTracks() if isinstance(via, pcbnew.PCB_VIA))):
                                valid = False
                            if valid:
                                place_marker(pt, layer)
        
        pcbnew.Refresh()
    ### find_angle
                                
                                

    def place_marker(pt, layer: str):
        board = pcbnew.GetBoard()
        marker = pcbnew.PCB_SHAPE(board)
        marker.SetShape(pcbnew.SHAPE_T_CIRCLE)
        marker.SetCenter(pcbnew.VECTOR2I(int(pt[0]), int(pt[1])))
        marker.SetRadius(pcbnew.FromMM(1))
        marker.SetLayer(getattr(pcbnew, layer))
        board.Add(marker)

    def clear_layer(layer: str):
        board = pcbnew.GetBoard()
        drawing_to_remove = [d for d in board.GetDrawings() if d.GetLayer() == getattr(pcbnew, layer)]
        for d in drawing_to_remove:
            board.Remove(d)
        pcbnew.Refresh()

    def seg_contained(inner, outer, tol=1000):
        if inner.GetNetCode() != outer.GetNetCode():
            return False

        x1, y1 = outer.GetStart().x, outer.GetStart().y
        x2, y2 = outer.GetEnd().x, outer.GetEnd().y
        px1, py1 = inner.GetStart().x, inner.GetStart().y
        px2, py2 = inner.GetEnd().x, inner.GetEnd().y

        dx, dy = x2 - x1, y2 - y1
        len_sq = dx * dx + dy * dy
        if len_sq == 0:
            return True

        length = math.sqrt(len_sq)

        dist1 = abs(dx * (py1 - y1) - dy * (px1 - x1)) / length
        dist2 = abs(dx * (py2 - y1) - dy * (px2 - x1)) / length

        if dist1 > tol or dist2 > tol:
            return False

        t1 = ((px1 - x1) * dx + (py1 - y1) * dy) / len_sq
        t2 = ((px2 - x1) * dx + (py2 - y1) * dy) / len_sq

        # 1. Catch exact duplicate overlapping tracks
        is_exact_duplicate = (
            (
                abs(px1 - x1) < tol
                and abs(py1 - y1) < tol
                and abs(px2 - x2) < tol
                and abs(py2 - y2) < tol
            )
            or (
                abs(px1 - x2) < tol
                and abs(py1 - y2) < tol
                and abs(px2 - x1) < tol
                and abs(py2 - y1) < tol
            )
        )
        if is_exact_duplicate:
            return True
    
        return (1e-3 < t1 < 0.999) and (1e-3 < t2 < 0.999)

    def filter_tracks(tracks):
        valid_tracks = [
            t
            for t in tracks
            if t.GetLength() > 0 and not isinstance(t, pcbnew.PCB_VIA)
        ]
        filtered_tracks = []

        for i, seg_a in enumerate(valid_tracks):
            contained = False
        for j, seg_b in enumerate(valid_tracks):
            if i == j:
                continue

            if seg_b.GetLength() > seg_a.GetLength() or (
                seg_b.GetLength() == seg_a.GetLength() and j < i
            ):
            # IF IT'S A WIDTH TRANSITION, DO NOT DELETE IT!
                if seg_a.GetWidth() != seg_b.GetWidth():
                    continue

            if seg_contained(seg_a, seg_b):
                contained = True
                break

        if not contained:
            filtered_tracks.append(seg_a)

        return filtered_tracks
        
## class FindAngle

find_angle = FindAngle.find_angle
place_marker = FindAngle.place_marker
clear_layer = FindAngle.clear_layer
seg_contained = FindAngle.seg_contained
filter_tracks = FindAngle.filter_tracks