#!/usr/bin/env python3
"""
Notebook rendering fix for MuJoCo issues.
Run this cell in your notebook to fix rendering problems.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML

def fix_mujoco_rendering():
    """
    Try to fix MuJoCo rendering by setting different GL backends.
    """
    # Try different MuJoCo GL backends
    gl_backends = ['osmesa', 'glfw', 'egl', 'disable']
    
    for backend in gl_backends:
        try:
            os.environ['MUJOCO_GL'] = backend
            print(f"✓ Trying MUJOCO_GL={backend}")
            
            # Test if this backend works
            import mujoco
            
            # Create a simple test model
            xml_string = """
            <mujoco>
              <worldbody>
                <geom type="sphere" size="0.1" pos="0 0 0"/>
              </worldbody>
            </mujoco>
            """
            
            model = mujoco.MjModel.from_xml_string(xml_string)
            data = mujoco.MjData(model)
            
            # Try to create a renderer
            renderer = mujoco.Renderer(model, height=240, width=240)
            print(f"✓ Successfully set MUJOCO_GL={backend}")
            return True
            
        except Exception as e:
            print(f"❌ MUJOCO_GL={backend} failed: {e}")
    
    print("⚠️  All MuJoCo GL backends failed. Using alternative visualization.")
    return False

def create_simple_visualization(ang, filename='trajectory_analysis.png'):
    """
    Create a simple visualization of the trajectory data using matplotlib.
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot joint angles over time
    axes[0, 0].plot(ang)
    axes[0, 0].set_title('Joint Angles Over Time')
    axes[0, 0].set_xlabel('Frame')
    axes[0, 0].set_ylabel('Angle (radians)')
    
    # Plot specific joints (e.g., knees)
    if ang.shape[1] >= 17:  # Make sure we have enough joints
        axes[0, 1].plot(ang[:, [9, 16]])  # Assuming joints 9 and 16 are knees
        axes[0, 1].set_title('Knee Angles')
        axes[0, 1].set_xlabel('Frame')
        axes[0, 1].set_ylabel('Angle (radians)')
        axes[0, 1].legend(['Left Knee', 'Right Knee'])
    else:
        # Plot first two joints if we don't have enough
        axes[0, 1].plot(ang[:, :2])
        axes[0, 1].set_title('First Two Joint Angles')
        axes[0, 1].set_xlabel('Frame')
        axes[0, 1].set_ylabel('Angle (radians)')
    
    # Plot angle distributions
    axes[1, 0].hist(ang.flatten(), bins=50, alpha=0.7)
    axes[1, 0].set_title('Angle Distribution')
    axes[1, 0].set_xlabel('Angle (radians)')
    axes[1, 0].set_ylabel('Frequency')
    
    # Plot correlation matrix
    if ang.shape[1] > 1:
        corr_matrix = np.corrcoef(ang.T)
        im = axes[1, 1].imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        axes[1, 1].set_title('Joint Angle Correlations')
        plt.colorbar(im, ax=axes[1, 1])
    else:
        axes[1, 1].text(0.5, 0.5, 'Need multiple joints\nfor correlation plot', 
                        ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Joint Angle Correlations')
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ Saved plot to {filename}")
    
    plt.show()
    return fig

def alternative_render_trajectory(ang, filename='reconstruction.mp4'):
    """
    Alternative rendering function that creates a simple animation.
    """
    try:
        import matplotlib.animation as animation
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create a simple 3D trajectory visualization
        # Assuming ang contains joint angles, we'll create a simple skeleton
        frames = len(ang)
        
        def animate(frame):
            ax.clear()
            
            # Create a simple skeleton visualization
            # This is a placeholder - you might want to convert angles to positions
            t = frame / frames
            x = np.cos(2 * np.pi * t + ang[frame, 0] if len(ang[frame]) > 0 else 0)
            y = np.sin(2 * np.pi * t + ang[frame, 1] if len(ang[frame]) > 1 else 0)
            z = ang[frame, 2] if len(ang[frame]) > 2 else 0
            
            # Plot the trajectory point
            ax.scatter([x], [y], [z], c='red', s=100)
            
            # Plot the full trajectory up to this point
            if frame > 0:
                t_vals = np.linspace(0, frame/frames, frame+1)
                x_vals = [np.cos(2 * np.pi * t + ang[i, 0] if len(ang[i]) > 0 else 0) for i in range(frame+1)]
                y_vals = [np.sin(2 * np.pi * t + ang[i, 1] if len(ang[i]) > 1 else 0) for i in range(frame+1)]
                z_vals = [ang[i, 2] if len(ang[i]) > 2 else 0 for i in range(frame+1)]
                ax.plot(x_vals, y_vals, z_vals, 'b-', alpha=0.5)
            
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Trajectory Visualization - Frame {frame}')
            ax.set_xlim([-1.5, 1.5])
            ax.set_ylim([-1.5, 1.5])
            ax.set_zlim([np.min(ang[:, 2]) if ang.shape[1] > 2 else -1, 
                        np.max(ang[:, 2]) if ang.shape[1] > 2 else 1])
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=frames, 
                                     interval=50, blit=False)
        
        if filename:
            # Save as video
            anim.save(filename, writer='ffmpeg', fps=20)
            print(f"✓ Saved animation to {filename}")
        
        return anim
        
    except Exception as e:
        print(f"Animation creation failed: {e}")
        print("Falling back to simple plotting...")
        return create_simple_visualization(ang)

# Main execution
print("🔧 Fixing MuJoCo rendering...")
if fix_mujoco_rendering():
    print("✅ MuJoCo rendering is now working!")
    print("You can now use the original render_trajectory function.")
else:
    print("⚠️  MuJoCo rendering failed. Using alternative visualization.")
    print("Use the alternative_render_trajectory function instead.")

print("\n📊 Available functions:")
print("- create_simple_visualization(ang, filename): Creates static plots")
print("- alternative_render_trajectory(ang, filename): Creates animated visualization")
print("- fix_mujoco_rendering(): Tries to fix MuJoCo rendering")
