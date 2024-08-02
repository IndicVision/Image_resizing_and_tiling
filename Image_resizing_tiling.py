import os
import cv2
import argparse
import numpy as np

def warp_image(image, angle_range):
    rows, cols = image.shape[:2]

    # Random rotation angle within the specified range
    angle = np.random.uniform(-angle_range, angle_range)
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)

    # Apply the rotation
    rotated_image = cv2.warpAffine(image, M, (cols, rows))

    # Random perspective transform points
    pts1 = np.float32([[0, 0], [cols, 0], [0, rows], [cols, rows]])
    delta = np.random.uniform(-0.1, 0.1, (4, 2)) * np.array([cols, rows])
    pts2 = pts1 + delta.astype(np.float32)

    # Apply the perspective transform
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warped_image = cv2.warpPerspective(rotated_image, M, (cols, rows))

    return warped_image

def split_image_into_tiles(image, tile_size):
    tiles = []
    rows, cols = image.shape[:2]
    for i in range(0, rows, tile_size):
        for j in range(0, cols, tile_size):
            tile = image[i:i+tile_size, j:j+tile_size]
            tiles.append(tile)
    return tiles

def resize_images(input_folder, output_folder, resize_factors, warp, tile_flag, tile_size, angle_range):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get the base name of the input folder
    input_folder_name = os.path.basename(os.path.normpath(input_folder))

    # Get the list of all images in the input folder
    images = [img for img in os.listdir(input_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Process each image
    for img in images:
        img_path = os.path.join(input_folder, img)
        original_image = cv2.imread(img_path)

        # Save warped image if warp flag is True
        if warp:
            warped_image = warp_image(original_image, angle_range)
            warp_folder_name = f"{input_folder_name}_warped"
            warp_folder = os.path.join(output_folder, warp_folder_name)
            os.makedirs(warp_folder, exist_ok=True)
            warped_img_path = os.path.join(warp_folder, img)
            cv2.imwrite(warped_img_path, warped_image)
            print(f"Saved warped image at {warped_img_path}")

            # Tile the warped image if tile flag is True
            if tile_flag:
                tiles = split_image_into_tiles(warped_image, tile_size)
                tile_folder_name = f"{input_folder_name}_warped_tiles"
                tile_folder = os.path.join(output_folder, tile_folder_name)
                os.makedirs(tile_folder, exist_ok=True)
                for idx, tile in enumerate(tiles):
                    tile_img_path = os.path.join(tile_folder, f"{os.path.splitext(img)[0]}_tile_{idx}.png")
                    cv2.imwrite(tile_img_path, tile)
                    print(f"Saved tile image at {tile_img_path}")

        for factor in resize_factors:
            # Calculate new size
            new_width = int(original_image.shape[1] / factor)
            new_height = int(original_image.shape[0] / factor)
            resized_image = cv2.resize(original_image, (new_width, new_height))

            # Ensure the factor-specific folder exists
            factor_folder_name = f"{input_folder_name}_factor_{factor}"
            factor_folder = os.path.join(output_folder, factor_folder_name)
            os.makedirs(factor_folder, exist_ok=True)

            # Save the resized image
            resized_img_path = os.path.join(factor_folder, img)
            cv2.imwrite(resized_img_path, resized_image)
            print(f"Saved resized image at {resized_img_path}")

def main():
    parser = argparse.ArgumentParser(description='Resize and optionally warp images by specified factors.')
    parser.add_argument('input_folder', type=str, help='Path to the folder containing input images')
    parser.add_argument('output_folder', type=str, help='Path to the folder to store resized images')
    parser.add_argument('factors', nargs='+', type=int, help='Resize factors (e.g. 2 4 6)')
    parser.add_argument('--warp', action='store_true', help='If given, images will be warped to mimic human capture orientations')
    parser.add_argument('--angle_range', type=float, default=5, help='Range of angles for random warping (default: 30 degrees)')
    parser.add_argument('--tile', action='store_true', help='If given, warped images will be tiled')
    parser.add_argument('--tile_size', type=int, default=256, help='Size of each tile (default: 256)')
    

    args = parser.parse_args()

    resize_images(args.input_folder, args.output_folder, args.factors, args.warp, args.tile, args.tile_size, args.angle_range)

if __name__ == "__main__":
    main()
