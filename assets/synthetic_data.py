# Name: synthetic_data.py
# Author: Carter Hidalgo
#
# Purpose: [Archived] Generate labeled synthetic training data for an object detection model YOLOv8

import bpy
import os
import random
import math
import numpy as np

# Render parameters
DO_RENDER = True
MAX_RENDERS = 4890 # Max 4890 FENS in fens.txt
DEBUG = True

# "List" type data structures
imported_pieces = {} # For original imports from which copies can be made
instances = [] # For storing all instances (copies) of orig imports
    
# Directories
script_dir = os.path.dirname(bpy.data.filepath)
model_dir = os.path.join(script_dir, "chess-piece-files")
resources_dir = os.path.join(script_dir, "resources")
image_dir = os.path.join(script_dir, "images")
label_dir = os.path.join(script_dir, "labels")

# Board constants
SQUARE_SIZE = 1.0 # Board square size
POS_VARY = 0.1 # Variation on square placement
CEN_OFFSET = 3.5 # Offset models so the center of the board is at (0, 0, 0)


# Function to clear all orphan meshes (meshes with 0 users)
def clear_orphan_meshes():
    num_orph = 0

    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
            num_orph += 1

    bpy.context.view_layer.update()

    # if DEBUG:
    #     print(f"removed {num_orph} orphan mesh(es)")


# Function to set up a new camera if none exists
def setup_camera(height=14):
    camera = None
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            camera = obj

            if DEBUG:
                print("using existing camera")
            break

    if not camera:
        bpy.ops.object.camera_add()
        camera = bpy.context.active_object
        
        if DEBUG:
            print("creating a new camera")

    bpy.context.scene.camera = camera

    camera.location = (0, 0, height)
    camera.rotation_euler = (0, 0, math.radians(90))

    return camera


# Function to setup the textured plane that represents the backdrop
def setup_backdrop():
    existing_backdrop = bpy.data.objects.get("Backdrop")
    if existing_backdrop:
        if DEBUG:
            print("using existing backdrop")
        return
    
    if DEBUG:
        print("creating a new backdrop")
    bpy.ops.mesh.primitive_plane_add(size = 10, enter_editmode=False, align='WORLD', location=(0, 0, -0.1), rotation=(0,0,0))

    plane = bpy.context.active_object
    plane.name = "Backdrop"

    image = bpy.data.images.get("backdrop.jpg")
    if not image:
        image = bpy.data.images.load(os.path.join(resources_dir, "backdrop.jpg"))
    
    # Check if the material already exists
    material = bpy.data.materials.get("Backdrop_Material")
    if not material:
        material = bpy.data.materials.new(name="Backdrop_Material")
        material.use_nodes = True

        bsdf = material.node.tree.nodes.get("Principled BSDF")
        tex_image = material.node_tree.nodes.new("ShaderNodeTexImage")

        tex_image.image = image
        material.node_tree.links.new(tex_image.outputs[0], bsdf.inputs[0])
    
    if plane.data.materials:
        plane.data.materials[0] = material
    else:
        plane.data.materials.append(material)


# Function to setup the textured plane that represents the chess board
def setup_board():
    existing_plane = bpy.data.objects.get("Chess_Board")
    if existing_plane:
        if DEBUG:
            print("using existing board")
        return        

    if DEBUG:
        print("creating a new board")
    bpy.ops.mesh.primitive_plane_add(size=8, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(0, 0, math.radians(90)))
    
    plane = bpy.context.active_object
    plane.name = "Chess_Board"

    image = bpy.data.images.get("board.jpg")
    if not image:
        image = bpy.data.images.load(os.path.join(resources_dir, "board.jpg"))

    # Check if the material already exists
    material = bpy.data.materials.get("Board_Material")
    if not material:
        material = bpy.data.materials.new(name="Board_Material")
        material.use_nodes = True

        bsdf = material.node_tree.nodes.get("Principled BSDF")
        tex_image = material.node_tree.nodes.new("ShaderNodeTexImage")

        tex_image.image = image
        material.node_tree.links.new(tex_image.outputs[0], bsdf.inputs[0])

    if plane.data.materials:
        plane.data.materials[0] = material
    else:
        plane.data.materials.append(material)


# Function to import one of every piece type and hide away from the camera
def import_models():
    piece_map = {
        'r': 'rook.stl', 'n': 'knight.stl', 'b': 'bishop.stl', 'q': 'queen.stl', 'k': 'king.stl', 'p': 'pawn.stl',
    }
    name_map = {
        'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king', 'p': 'pawn',
    }
    num_copies = 0

    for piece, filename in piece_map.items():
        piece_name = name_map[piece.lower()]
        
        base_model = bpy.data.objects.get(piece_name)

        if base_model:
            copies = [obj for obj in bpy.data.objects if obj.name.startswith(piece_name + ".")]
            for copy in copies:
                num_copies += 1
                bpy.data.objects.remove(copy, do_unlink=True)

            # if DEBUG and num_copies != 0:
            #     print(f"removed {num_copies} {piece_name} copies")

            # print(f"skipped importing {piece_name}.stl because it already exists")
            
            imported_pieces[piece] = base_model
            continue
        
        piece_file = os.path.join(model_dir, filename)
        bpy.ops.wm.stl_import(filepath=piece_file)

        # if DEBUG:
        #     print(f"imported {piece_name} because none was found")

        imported_object = bpy.context.selected_objects[-1]
        imported_object.name = piece_name 

        imported_object.location = (20, 20, 0)
        imported_object.scale = (0.019, 0.019, 0.019)

        imported_pieces[piece] = imported_object


# Function to parse FEN string and return every piece type and rank/file board location
def parse_fen(fen):
    pieces = []
    rows = fen[1:].split('/')
    for row_index, row in enumerate(rows):
        col = 0
        for char in row:
            if char.isdigit():
                col += int(char)
            else:
                pieces.append((char, row_index, col))
                col += 1
    return pieces


# Function to get the real scene location using rank/file location
def get_real_loc(loc):
    return (loc[1] * SQUARE_SIZE + random.uniform(-POS_VARY, POS_VARY) - CEN_OFFSET, loc[2] * SQUARE_SIZE + random.uniform(-POS_VARY, POS_VARY) - CEN_OFFSET, 0)


# Function to place the chess pieces listed in a FEN into the real scene
def place_chess_pieces(fen):
    # if DEBUG:
    #     print("placing pieces/getting bounding boxes")

    labels = []
    instance_pieces = parse_fen(fen)

    black_material = bpy.data.materials.get("plc-plastic-black")
    white_material = bpy.data.materials.get("plc-plastic-white")

    if not black_material or not white_material:
        raise ValueError("Materials 'plc-plastic-black' or 'plc-plastic-white' not found.")

    for loc in instance_pieces:
        piece = imported_pieces[loc[0].lower()].copy() 
        piece.data = piece.data.copy() 
        instances.append(piece)
        bpy.context.collection.objects.link(piece)

        piece.location = get_real_loc(loc)
        piece.rotation_euler = (0, 0, random.uniform(math.radians(0), math.radians(360)))

        piece.data.materials.clear()
        if loc[0].isupper():
            piece.data.materials.append(white_material)
        else:
            piece.data.materials.append(black_material) 

        box = get_label(bpy.context.scene, bpy.context.scene.camera, piece, loc[0])
        labels.append(box)

    bpy.context.view_layer.update() 

    return labels


# Function for clearing all instances of a model
def clear_instances():
    bpy.ops.object.select_all(action='DESELECT')
    
    for obj in instances:
        obj.select_set(True)

    bpy.ops.object.delete()

    # if DEBUG:
    #     print(f"removed {len(instances)} instances")

    instances.clear()

    clear_orphan_meshes()

    bpy.context.view_layer.update()


# Function to render image
def render_image(output_path, image_name):
    bpy.context.scene.render.filepath = os.path.join(output_path, image_name)
    bpy.ops.render.render(write_still=True)


# Function to write bounding box data to a txt file for YOLO
def write_boxes(bounding_boxes, filename):
    file_path = os.path.join(label_dir, filename)

    with open(file_path, 'w') as f:
        for bbox in bounding_boxes:
            line = ' '.join(map(str, bbox))
            f.write(line + '\n')
    
    # print(f"wrote {len(bounding_boxes)} lines to {filename}")


# Function to load the fen strings from file
def load_fens():
    fens_file = os.path.join(resources_dir, "fens.txt")
    if not os.path.isfile(fens_file):
        print(f"FEN file not found: {fens_file}")
        return
    
    with open(fens_file, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]
    
    if not fens:
        print("No FEN strings found in FENS.txt")
        return


# Function to obtain a render of a fen string
def render_fen(fen, count):
    labels = place_chess_pieces(fen)

    if DO_RENDER:
        if DEBUG:
            print(f"rendering {fen}")
        image_name = f"chess_{count + 1}.png"
        label_name = f"chess_{count + 1}.txt"
        
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        render_image(image_dir, image_name)

        if not os.path.exists(label_dir):
            os.makedirs(label_dir)
        
        # send labels to chess_{count + 1}.txt
        write_boxes(labels, label_name)
    # else:
    #     print("\"Pseudo-rendering...\"")

    # Obliterate all piece instances
    clear_instances()

    # Print progress to console
    print(f"{count+1}/{MAX_RENDERS}")

def get_class(piece):
    # 0  -> blackPawn
    # 1  -> blackKnight
    # 2  -> blackBishop
    # 3  -> blackRook
    # 4  -> blackQueen
    # 5  -> blackKing
    # 6  -> whitePawn
    # 7  -> whiteKnight
    # 8  -> whiteBishop
    # 9  -> whiteRook
    # 10 -> whiteQueen
    # 11 -> whiteKing
    class_map = {
        'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5, 'P': 6, 'N': 7, 'B': 8, 'R': 9, 'Q': 10, 'K': 11,
    }

    return class_map[piece]

def get_label(scene, cam_ob, obj, code):
    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = obj.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(obj.matrix_world)
    me.transform(mat)

    camera = cam_ob.data

    def _get_coords():
        frame = [-v for v in camera.view_frame(scene=scene)[:3]]
        for v in me.vertices:
            co_local = v.co
            z = -co_local.z

            if z <= 0.0:
                continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

            min_x, max_x = frame[1].x, frame[2].x
            min_y, max_y = frame[0].y, frame[1].y

            x = (co_local.x - min_x) / (max_x - min_x)
            y = (co_local.y - min_y) / (max_y - min_y)

            yield x, y

    xs, ys = np.array(list(_get_coords())).T

    min_x = np.clip(min(xs), 0.0, 1.0)
    max_x = np.clip(max(xs), 0.0, 1.0)
    min_y = np.clip(min(ys), 0.0, 1.0)
    max_y = np.clip(max(ys), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    width = (max_x - min_x) * dim_x
    height = (max_y - min_y) * dim_y
    center_x = (min_x + (width / dim_x) / 2.0) * dim_x
    center_y = dim_y - ((min_y + (height / dim_y) / 2.0) * dim_y)

    return (get_class(code), (center_x / 1080), (center_y / 1080), (width / 1080), (height / 1080))


# Main function
def main():
    print("\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    clear_orphan_meshes()
    setup_camera()
    setup_board()
    setup_backdrop()
    import_models()

    render_count = 0

    for fen in load_fens():
        if render_count >= MAX_RENDERS:
            break
        
        render_fen(fen, render_count)
        render_count += 1

    print(f"Script complete. {render_count} image(s) saved")

if __name__ == "__main__":
    main()
