import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import sys
import os

def compare_images(image_path1, image_path2):
    if not os.path.exists(image_path1):
        print(f"Error: {image_path1} not found.")
        return
    if not os.path.exists(image_path2):
        print(f"Error: {image_path2} not found.")
        return

    # Load images
    img1 = Image.open(image_path1).convert('RGB')
    img2 = Image.open(image_path2).convert('RGB')
    
    # Convert to numpy arrays
    data1 = np.array(img1)
    data2 = np.array(img2)
    
    # Create subplots: 2x2 grid
    # Top Left: Red, Top Right: Green
    # Bottom Left: Blue, Bottom Right: Spatial Difference Image
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Steganography Analysis\n{os.path.basename(image_path1)} vs {os.path.basename(image_path2)}')
    
    # Flatten axes for easy iteration
    flat_axes = axes.flatten()
    
    colors = ['r', 'g', 'b']
    channel_names = ['Red', 'Green', 'Blue']
    
    # Plot Histograms for R, G, B
    for i, channel in enumerate(channel_names):
        ax = flat_axes[i]
        
        # Explicit bins
        bins = range(257)
        hist1, _ = np.histogram(data1[:,:,i].ravel(), bins=bins)
        hist2, _ = np.histogram(data2[:,:,i].ravel(), bins=bins)
        
        # Plot Image 1 (Blue)
        ax.plot(hist1, color='blue', alpha=0.9, label='Image 1', linewidth=1.5)
        ax.fill_between(range(256), hist1, color='blue', alpha=0.1)
        
        # Plot Image 2 (Red)
        ax.plot(hist2, color='red', alpha=0.9, label='Image 2', linewidth=1.5)
        
        # Plot Difference (Green)
        # Calculate diff: how much bin count changed
        diff = hist2 - hist1
        # We plot diff relative to 0. We might want to plot it on a secondary axis if huge, 
        # but for steg it's usually small. Let's create a twinx axis for it to be visible.
        ax2 = ax.twinx()
        ax2.bar(range(256), diff, color='green', alpha=0.3, label='Count Diff (Img2 - Img1)')
        ax2.set_ylabel('Difference Count', color='green')
        ax2.tick_params(axis='y', labelcolor='green')
        
        ax.set_ylabel('Pixel Count')
        ax.set_xlabel('Pixel Value (0-255)')
        
        # Combine legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        
        ax.set_title(f'{channel} Channel Distribution')
        ax.grid(True, alpha=0.3)

    # Plot Spatial Difference Image in the 4th slot (bottom right)
    ax_diff = flat_axes[3]
    
    # Calculate absolute difference per pixel (sum of absolute diffs across channels)
    # Convert to int16 to avoid overflow/underflow during subtraction, then abs
    diff_image = np.abs(data1.astype(np.int16) - data2.astype(np.int16))
    # Sum across RGB channels to get a single intensity map of differences
    diff_map = np.sum(diff_image, axis=2)
    
    # Amplify the difference for visibility (steg changes are often 1/255, invisible)
    # We will scale the max difference to 255 for display
    if diff_map.max() > 0:
        scale_factor = 255.0 / diff_map.max()
        display_diff = (diff_map * scale_factor).astype(np.uint8)
        title_extra = f"(Amplified x{scale_factor:.1f})"
    else:
        display_diff = diff_map.astype(np.uint8)
        title_extra = "(No Differences)"

    ax_diff.imshow(display_diff, cmap='hot')
    ax_diff.set_title(f'Spatial Difference Map {title_extra}')
    ax_diff.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Example usage: Replace with your actual file paths
    # You can pass arguments via command line or edit these variables
    if len(sys.argv) == 3:
        img1 = sys.argv[1]
        img2 = sys.argv[2]
    else:
        # Default placeholders - CHANGE THESE
        print("Usage: python image_testing.py <image1_path> <image2_path>")
        print("Using default/test paths if they exist...")
        img1 = "/Users/lakshmisashank/Desktop/Steganography/testing/img.jpeg" 
        img2 = "/Users/lakshmisashank/Downloads/img_steg.png" 
    
    compare_images(img1, img2)
