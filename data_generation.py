
import numpy as np
import pandas as pd

def project_point(camera_pos, look_at, point, up_hint=np.array([0,1,0])):
    """
    Project a 3D point into a 2D image plane for a camera.
    Constructs a camera coordinate system using:
      - view_dir: normalized vector from camera_pos to look_at.
      - right: computed from the cross product of up_hint and view_dir.
      - up: recomputed to ensure orthogonality.
    Returns the (x, y) coordinates on the image plane.
    """
    # Compute view direction (camera's z-axis)
    view_dir = look_at - camera_pos
    view_dir = view_dir / np.linalg.norm(view_dir)
    
    # Adjust up_hint if too parallel to view_dir
    if np.abs(np.dot(view_dir, up_hint)) > 0.99:
        up_hint = np.array([0, 0, 1])
    
    # Compute the right (x-axis) and then the up (y-axis)
    right = np.cross(up_hint, view_dir)
    right = right / np.linalg.norm(right)
    up = np.cross(view_dir, right)
    up = up / np.linalg.norm(up)
    
    # Compute projection by dotting the relative vector with right and up
    rel = point - camera_pos
    x_proj = np.dot(rel, right)
    y_proj = np.dot(rel, up)
    return np.array([x_proj, y_proj]), np.array([right,up])

    

def mass_top(t):
    """
    Returns the 3D position of the top of the mass at time t.
    The mass oscillates vertically:
        z(t) = 0.5 * cos(2*pi*0.5*t)
    """
    z = 0.5 * np.cos(2 * np.pi * 0.5 * t)
    return np.array([0, 0, z])



def data_gen():
    # Generate the 2D projections for each camera.
    # Each camera provides two time series: one for x and one for y.
    data = {}
    
    # Each camera is positioned to provide distinct x and y projections.
    cameras = {
        "Camera_1": np.array([0, 0, -2]),
        "Camera_2": np.array([5, 2.5, 0.5]),
        "Camera_3": np.array([1.5, -1.5, 0.5])
    }
    
    look_at = np.array([0, 0, 0])

    # Time values for the simulation.
    t_values = np.linspace(0, 3, 100)

    for cam_name, cam_pos in cameras.items():
        x_series = []
        y_series = []
        for t in t_values:
            pt3d = mass_top(t)
            pt2d, axs = project_point(cam_pos, look_at, pt3d)
            x_series.append(pt2d[0])
            y_series.append(pt2d[1])
        data[cam_name] = {"x": np.array(x_series), "y": np.array(y_series), "x_axis": axs[0], "y_axis": axs[1]}
        
    return data , t_values

