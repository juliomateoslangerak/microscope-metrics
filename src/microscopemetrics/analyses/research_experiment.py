from getpass import getpass

import numpy as np
import omero_toolbox as ot
from omero.model import Point
from skimage import data
from skimage.transform import rescale

username = "mateos"
HOST = "omero.mri.cnrs.fr"
PORT = 4064
GROUP = "MRI-COMMUN"
dataset_id = 25502


try:
    # Open the connection to OMERO
    conn = ot.open_connection(
        username=str(input(f"Username ({username}): ") or username),
        password=getpass("OMERO Password: ", None),
        host=str(input("server (omero.mri.cnrs.fr): ") or HOST),
        port=int(input("port (4064): ") or PORT),
        group=str(input(f"Group ({GROUP}): ") or GROUP),
    )

    dataset_id = int(input("Dataset ID: ") or dataset_id)

    dataset = ot.get_dataset(conn, dataset_id)
    images = dataset.listChildren()

    roi_service = conn.getRoiService()

    for image in images:
        image_intensities = None
        pixel_size = ot.get_pixel_size(image, order="zyx")

        rois = roi_service.findByImage(image.getId(), None).rois
        for roi in rois:
            shape = roi.getPrimaryShape()
            if isinstance(shape, Point):
                try:
                    z_pos = shape.getTheZ()._val
                except AttributeError:
                    z_pos = 0
                try:
                    t_pos = shape.getTheT()._val
                except AttributeError:
                    t_pos = 0
                try:
                    c_pos = shape.getTheC()._val
                except AttributeError:
                    c_pos = 0
                y_pos = shape.getY()._val
                x_pos = shape.getX()._val
                try:
                    shape_comment = shape.getTextValue()._val
                except AttributeError:
                    shape_comment = f"Point_{z_pos}_{c_pos}_{t_pos}_{y_pos:.2f}_{x_pos:.2f}"

                if image_intensities is None:
                    image_intensities = ot.get_intensities(image)

                # dims in order z, c, t, y, x
                yx_slice = image_intensities[z_pos, c_pos, t_pos, :, :]
                yx_slice = np.reshape(yx_slice, (1, 1, 1, yx_slice.shape[0], yx_slice.shape[1]))
                yx_image = ot.create_image_from_numpy_array(
                    connection=conn,
                    data=yx_slice,
                    image_name=f"{image.getName()}_{shape_comment}_yx",
                    image_description=f"yx Orthogonal slice at Z={z_pos}, C={c_pos}, T={t_pos}. source image: imageId={image.getId()}",
                    # channel_labels=None,
                    dataset=dataset,
                    source_image_id=image.getId(),
                    # channels_list=None,
                    # force_whole_planes=False
                )
                yx_image.unload()
                yx_line_roi = ot.create_roi(
                    connection=conn,
                    image=yx_image,
                    shapes=[
                        ot.create_shape_line(
                            x1_pos=0,
                            y1_pos=y_pos,
                            x2_pos=yx_slice.shape[4],
                            y2_pos=y_pos,
                            stroke_color=(255, 0, 0, 200),
                            stroke_width=0.5,
                        ),
                        ot.create_shape_line(
                            x1_pos=x_pos,
                            y1_pos=0,
                            x2_pos=x_pos,
                            y2_pos=yx_slice.shape[3],
                            stroke_color=(255, 0, 0, 200),
                            stroke_width=0.5,
                        ),
                    ],
                )

                zx_slice = image_intensities[:, c_pos, t_pos, int(y_pos), :]
                zx_slice = rescale(
                    zx_slice,
                    (pixel_size[0] / pixel_size[2], 1),
                    anti_aliasing=True,
                    preserve_range=True,
                )
                zx_slice = zx_slice.astype(image_intensities.dtype)
                zx_slice = np.reshape(zx_slice, (1, 1, 1, zx_slice.shape[0], zx_slice.shape[1]))
                zx_image = ot.create_image_from_numpy_array(
                    connection=conn,
                    data=zx_slice,
                    image_name=f"{image.getName()}_{shape_comment}_zx",
                    image_description=f"zx Orthogonal slice at Z={z_pos}, C={c_pos}, T={t_pos}. source image: imageId={image.getId()}",
                    # channel_labels=None,
                    dataset=dataset,
                    source_image_id=image.getId(),
                    # channels_list=None,
                    # force_whole_planes=False
                )
                zx_image.unload()
                zx_line_roi = ot.create_roi(
                    connection=conn,
                    image=zx_image,
                    shapes=[
                        ot.create_shape_line(
                            x1_pos=0,
                            y1_pos=(z_pos - 0.5) * (pixel_size[0] / pixel_size[2]),
                            x2_pos=zx_slice.shape[4],
                            y2_pos=(z_pos - 0.5) * (pixel_size[0] / pixel_size[2]),
                            stroke_color=(255, 0, 0, 200),
                            stroke_width=0.5,
                        ),
                        ot.create_shape_line(
                            x1_pos=x_pos,
                            y1_pos=0,
                            x2_pos=x_pos,
                            y2_pos=zx_slice.shape[3],
                            stroke_color=(255, 0, 0, 200),
                            stroke_width=0.5,
                        ),
                    ],
                )

                zy_slice = image_intensities[:, c_pos, t_pos, :, int(x_pos)]
                zy_slice = rescale(
                    zy_slice,
                    (pixel_size[0] / pixel_size[1], 1),
                    anti_aliasing=True,
                    preserve_range=True,
                )
                zy_slice = zy_slice.astype(image_intensities.dtype)
                zy_slice = np.transpose(
                    zy_slice, (1, 0)
                )  # Transpose to get the correct orientation
                zy_slice = np.reshape(zy_slice, (1, 1, 1, zy_slice.shape[0], zy_slice.shape[1]))
                zy_image = ot.create_image_from_numpy_array(
                    connection=conn,
                    data=zy_slice,
                    image_name=f"{image.getName()}_{shape_comment}_zy",
                    image_description=f"zy Orthogonal slice at Z={z_pos}, C={c_pos}, T={t_pos}. source image: imageId={image.getId()}",
                    # channel_labels=None,
                    dataset=dataset,
                    source_image_id=image.getId(),
                    # channels_list=None,
                    # force_whole_planes=False
                )
                zy_image.unload()
                zy_line_roi = ot.create_roi(
                    connection=conn,
                    image=zy_image,
                    shapes=[
                        ot.create_shape_line(
                            x1_pos=0,
                            y1_pos=y_pos,
                            x2_pos=zy_slice.shape[4],
                            y2_pos=y_pos,
                            stroke_color=(255, 0, 0, 200),
                            stroke_width=0.5,
                        ),
                        ot.create_shape_line(
                            x1_pos=(z_pos - 0.5) * (pixel_size[0] / pixel_size[1]),
                            y1_pos=0,
                            x2_pos=(z_pos - 0.5) * (pixel_size[0] / pixel_size[1]),
                            y2_pos=zy_slice.shape[3],
                            stroke_color=(255, 0, 0, 200),
                            stroke_width=0.5,
                        ),
                    ],
                )

finally:
    conn.close()
    print("Done")
