import os
import json
import geopandas as gpd
from shapely.geometry import Polygon, box
from pathlib import Path
from dotenv import load_dotenv

def transform_points(points, img_bbox, img_width, img_height):
    """
    Convert pixel coordinates (x, y) to geospatial coordinates using the bounding box of the image.
    """
    xmin, ymin, xmax, ymax = img_bbox.bounds
    x_scale = (xmax - xmin) / img_width
    y_scale = (ymax - ymin) / img_height

    return [0.
        (xmin + x * x_scale, ymax - y * y_scale)  # Flip y-axis
        for x, y in points
    ]


def process_json_and_save_shapefile(shapefile_path, folder_path, output_shapefile):
    tiles_df = gpd.read_file(shapefile_path)

    if "TileID" not in tiles_df.columns or tiles_df.geometry is None:
        print("Error: The shapefile must have a 'TileID' column and valid geometries.")
        return

    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    transformed_shapes = []

    for json_file in json_files:
        tile_id = json_file.replace('.json', '')
        tile_row = tiles_df[tiles_df["TileID"] == tile_id]

        if tile_row.empty:
            print(f"Skipping {json_file}: No matching TileID in shapefile.")
            continue

        img_bbox = tile_row.geometry.iloc[0].bounds

        json_path = os.path.join(folder_path, json_file)
        with open(json_path, 'r') as f:
            data = json.load(f)

        img_width = data.get("imageWidth", None)
        img_height = data.get("imageHeight", None)

        if img_width is None or img_height is None:
            print(f"Skipping {json_file}: Missing image width/height metadata.")
            continue

        for shape in data.get('shapes', []):
            label = shape.get('label', 'No label')
            points = shape.get('points', [])

            transformed_points = transform_points(points, box(*img_bbox), img_width, img_height)

            if len(transformed_points) == 2:  # Convert two points into a rectangle
                (x1, y1), (x2, y2) = transformed_points
                polygon = box(x1, y1, x2, y2)
            elif len(transformed_points) >= 3:
                polygon = Polygon(transformed_points)
            else:
                continue

            transformed_shapes.append({"geometry": polygon, "Label": label})

    if transformed_shapes:
        gdf = gpd.GeoDataFrame(transformed_shapes, crs=tiles_df.crs)
        gdf.to_file(output_shapefile)
        print(f"Transformed polygons saved to: {output_shapefile}")
    else:
        print("No valid shapes found. No shapefile was created.")


if __name__ == "__main__":
    
    
    
    load_dotenv()
    outputfolder = Path(os.environ['workdirectory'])
    output_shapefile = outputfolder / "Labels.shp"

    workdirectory = Path(os.environ['workdirectory'])
    folder_path = workdirectory / 'Images' / 'All'
    shapefile_path = workdirectory / 'Tiles_ortho.shp'

    process_json_and_save_shapefile(shapefile_path, folder_path, output_shapefile)
