import os
import cv2
import numpy as np


DATA_ROOT  =  '../data'


def fill_with_ellipses(binary_mask_path, output_path = None,
                       output_overlay_path = None, min_area = 50):
    # Read the binary mask
    mask  =  cv2.imread(binary_mask_path, cv2.IMREAD_GRAYSCALE)
    # print(mask.shape)
    _, mask  =  cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    # Find contours of the white regions
    contours, _  =  cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an empty output mask
    ellipse_mask = np.zeros_like(mask)

    for cnt in contours:
        # Skip very small regions (noise)
        if cv2.contourArea(cnt) < min_area:
            continue

        if len(cnt) < 5:
            continue  # Need at least 5 points to fit an ellipse

        # Fit an ellipse to the contour
        ellipse = cv2.fitEllipse(cnt)
        # Draw the filled ellipse
        cv2.ellipse(ellipse_mask, ellipse, 255, -1)

    # Ensure the result is uint8 before saving
    ellipse_mask = ellipse_mask.astype(np.uint8)

    # Save or return result
    if output_path:
        cv2.imwrite(output_path, ellipse_mask)

    # Draw only the ellipse edge (red color, thickness 2)
    # Convert grayscale mask to BGR for color overlay
    overlay = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.ellipse(overlay, ellipse, (0, 0, 255), 2)
    # Save and return
    if output_overlay_path:
        cv2.imwrite(output_overlay_path, overlay)

    return ellipse_mask

# Example usage
in_img = DATA_ROOT + '/pred_Patient01726_Plane3_1_of_2.png'
out_img = DATA_ROOT + '/pred_Patient01726_Plane3_1_of_2_postprocessing.png'
out_overlay_img = DATA_ROOT + '/pred_Patient01726_Plane3_1_of_2_postprocessing_overlay.png'
result = fill_with_ellipses(in_img, out_img, out_overlay_img)
