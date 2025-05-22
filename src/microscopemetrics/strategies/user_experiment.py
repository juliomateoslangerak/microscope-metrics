# import random
#
# import numpy as np
# import pandas as pd
#
# try:
#     from hypothesis import assume
#     from hypothesis import strategies as st
# except ImportError as e:
#     raise ImportError(
#         "In order to run the strategies you need to install the test extras. Run `pip install microscopemetrics[test]`."
#     ) from e
# import microscopemetrics_schema.strategies.analyses as st_mm_analyses_schema
# from skimage.exposure import rescale_intensity as skimage_rescale_intensity
# from skimage.filters import gaussian as skimage_gaussian
# from skimage.util import random_noise as skimage_random_noise
#
# from microscopemetrics.analyses import numpy_to_mm_image
#
#
# # Strategies for user experiment
# def _gen_user_experiment_channel(
#     z_shape: int,
#     y_shape: int,
#     x_shape: int,
#     t_shape: int,
#     lines_nr: int,
#     sigma: float,
#     target_min_intensity: float,
#     target_max_intensity: float,
#     do_noise: bool,
#     signal: int,
# ) -> np.ndarray:
#     # Generate the channel as float64
#     channel = np.zeros(shape=(t_shape, z_shape, y_shape, x_shape), dtype="float64")
#
#     # draw lines_nr lines through the center of the image in z across the y and x dimensions
#     for i in range(lines_nr):
#         channel[
#             :,  # Time
#             int(channel.shape[0] * 0.5),  # Z
#             :,  # Y
#             int(channel.shape[2] * i / lines_nr),  # X
#         ] = 1.0
#         channel[
#             :,
#             int(channel.shape[0] * 0.5),
#             int(channel.shape[1] * i / lines_nr),
#             :,
#         ] = 1.0
#         channel[
#             :,
#             :,
#             int(channel.shape[1] * i / lines_nr),
#             int(channel.shape[1] * i / lines_nr),
#         ] = 1.0
#
#     channel = skimage_gaussian(
#         channel,
#         sigma=sigma,
#         mode="constant",
#         preserve_range=True,
#     )
#
#     # Normalize channel intensity to be between target_min_intensity and target_max_intensity
#     # Saturation point is at 1.0 when we rescale later to the target dtype
#     channel = skimage_rescale_intensity(
#         channel, out_range=(target_min_intensity, target_max_intensity)
#     )
#
#     if do_noise:
#         # The noise on a 1.0 intensity image is too strong, so we rescale the image to
#         # the defined signal and then rescale it back to the target intensity
#         channel = channel * signal
#         channel = skimage_random_noise(channel, mode="poisson", clip=False)
#         channel = channel / signal
#
#     return channel
#
#
# def _gen_user_experiment_image(
#     z_shape: int,
#     y_shape: int,
#     x_shape: int,
#     c_shape: int,
#     lines_nr: list[int],
#     sigma: list[float],
#     target_min_intensity: list[float],
#     target_max_intensity: list[float],
#     do_noise: bool,
#     signal: list[int],
#     dtype: np.dtype,
#     t_shape: int = 1,  # Added the time dimension here. Not used in the function yet
# ) -> np.ndarray:
#     # Generate the image as float64
#     image = np.zeros(shape=(t_shape, z_shape, y_shape, x_shape, c_shape), dtype="float64")
#
#     for ch in range(c_shape):
#         image[..., ch] = _gen_user_experiment_channel(
#             z_shape=z_shape,
#             y_shape=y_shape,
#             x_shape=x_shape,
#             t_shape=t_shape,
#             lines_nr=lines_nr[ch],
#             sigma=sigma[ch],
#             target_min_intensity=target_min_intensity[ch],
#             target_max_intensity=target_max_intensity[ch],
#             do_noise=do_noise,
#             signal=signal[ch],
#         )
#
#     # Rescale to the target dtype
#     image = np.clip(image, None, 1)
#     image = skimage_rescale_intensity(image, in_range=(0.0, 1.0), out_range=dtype)
#
#     return image
#
#
# @st.composite
# def st_user_experiment_test_data(
#     draw,
#     nr_images=st.integers(min_value=1, max_value=3),
#     z_image_shape=st.integers(min_value=2, max_value=50),
#     y_image_shape=st.integers(min_value=512, max_value=1024),
#     x_image_shape=st.integers(min_value=512, max_value=1024),
#     c_image_shape=st.integers(min_value=1, max_value=3),
#     lines_nr=st.integers(min_value=3, max_value=7),
#     dtype=st.sampled_from([np.uint8, np.uint16, np.float32]),
#     do_noise=st.just(True),
#     signal=st.floats(min_value=20.0, max_value=1000.0),
#     target_min_intensity=st.floats(min_value=0.001, max_value=0.1),
#     target_max_intensity=st.floats(min_value=0.5, max_value=0.9),
#     sigma=st.floats(min_value=2.0, max_value=10.0),
#     nr_orthogonal_rois=st.integers(min_value=0, max_value=3),
#     nr_profile_rois=st.integers(min_value=0, max_value=3),
# ) -> dict:
#     output = {
#         "images": [],
#         "lines_nr": [],
#         "orthogonal_rois": [],
#         "profile_rois": [],
#         "do_noise": [],
#         "signals": [],
#     }
#
#     c_image_shape = draw(c_image_shape)
#     z_image_shape = draw(z_image_shape)
#     y_image_shape = draw(y_image_shape)
#     x_image_shape = draw(x_image_shape)
#
#     do_noise = draw(do_noise)
#
#     dtype = draw(dtype)
#
#     for _ in range(draw(nr_images)):
#         image_target_min_intensities = [draw(target_min_intensity) for _ in range(c_image_shape)]
#         image_target_max_intensities = [draw(target_max_intensity) for _ in range(c_image_shape)]
#         image_sigma = [draw(sigma) for _ in range(c_image_shape)]
#         image_signals = [draw(signal) for _ in range(c_image_shape)]
#         image_lines_nr = [draw(lines_nr) for _ in range(c_image_shape)]
#
#         image = _gen_user_experiment_image(
#             z_shape=z_image_shape,
#             y_shape=y_image_shape,
#             x_shape=x_image_shape,
#             c_shape=c_image_shape,
#             lines_nr=image_lines_nr,
#             sigma=image_sigma,
#             target_min_intensity=image_target_min_intensities,
#             target_max_intensity=image_target_max_intensities,
#             do_noise=do_noise,
#             signal=image_signals,
#             dtype=dtype,
#         )
#
#         orthogonal_rois = []
#         for _ in range(draw(nr_orthogonal_rois)):
#             ortho_roi = st_mm_schema.st_mm_roi(
#                 shapes=[
#                     st_mm_schema.st_mm_point(
#                         c=st.just(None),
#                         t=st.just(None),
#                         z=st.floats(
#                             min_value=0.0,
#                             max_value=z_image_shape - 1,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                         y=st.floats(
#                             min_value=0.0,
#                             max_value=y_image_shape - 1,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                         x=st.floats(
#                             min_value=0.0,
#                             max_value=x_image_shape - 1,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                     )
#                 ]
#             )
#             orthogonal_rois.append(ortho_roi)
#
#         profile_rois = []
#         for _ in range(draw(nr_profile_rois)):
#             profile_roi = st_mm_schema.st_mm_roi(
#                 shapes=[
#                     st_mm_schema.st_mm_line(
#                         c=st.just(None),
#                         t=st.just(None),
#                         z=st.floats(
#                             min_value=0.0,
#                             max_value=z_image_shape - 1,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                         x1=st.floats(
#                             min_value=0.0,
#                             max_value=x_image_shape / 2,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                         x2=st.floats(
#                             min_value=x_image_shape / 2,
#                             max_value=x_image_shape - 1,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                         y1=st.floats(
#                             min_value=0.0,
#                             max_value=y_image_shape / 2,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                         y2=st.floats(
#                             min_value=y_image_shape / 2,
#                             max_value=y_image_shape - 1,
#                             exclude_min=True,
#                             exclude_max=True,
#                         ),
#                     )
#                 ]
#             )
#
#         output["images"].append(image)
#         output["lines_nr"].append(image_lines_nr)
#         output["do_noise"].append(do_noise)
#         output["signals"].append(image_signals)
#         output["orthogonal_rois"].append(orthogonal_rois)
#         output["profile_rois"].append(profile_rois)
#
#     return output
#
#
# @st.composite
# def st_user_experiment_dataset(
#     draw,
#     unprocessed_dataset=st_mm_analyses_schema.st_mm_user_experiment_unprocessed_dataset(),
#     test_data=st_user_experiment_test_data(),
# ):
#     test_data = draw(test_data)
#     user_experiment_unprocessed_dataset = draw(unprocessed_dataset)
#
#     # the unprocessed dataset contains one empty image, we need to delete it
#     user_experiment_unprocessed_dataset.input_data.user_experiment_images = []
#
#     for i, image in enumerate(test_data.pop("images")):
#         mm_image = numpy_to_mm_image(
#             array=image,
#             name=f"UE_image_{i}",
#             channel_names=[f"Channel_{i}{j}" for j in range(image.shape[-1])],
#         )
#
#         orthogonal_rois = test_data["orthogonal_rois"][i]
#         for ortho_roi in orthogonal_rois:
#             ortho_roi.linked_references.append(mm_image.data_reference)
#
#         profile_rois = test_data["profile_rois"][i]
#         for prof_roi in profile_rois:
#             prof_roi.linked_references.append(mm_image.data_reference)
#
#         user_experiment_unprocessed_dataset.input_data.user_experiment_images.append(mm_image)
#         user_experiment_unprocessed_dataset.input_data.orthogonal_rois.extend(orthogonal_rois)
#         user_experiment_unprocessed_dataset.input_data.profile_rois.extend(profile_rois)
#
#     # Setting the bit depth to the data type of the image
#     image_dtype = {
#         a.array_data.dtype
#         for a in user_experiment_unprocessed_dataset.input_data.user_experiment_images
#     }
#     if len(image_dtype) != 1:
#         raise ValueError("All images should have the same data type")
#     image_dtype = image_dtype.pop()
#     if np.issubdtype(image_dtype, np.integer):
#         user_experiment_unprocessed_dataset.input_parameters.bit_depth = np.iinfo(image_dtype).bits
#     elif np.issubdtype(image_dtype, np.floating):
#         user_experiment_unprocessed_dataset.input_parameters.bit_depth = np.finfo(image_dtype).bits
#     else:
#         user_experiment_unprocessed_dataset.input_parameters.bit_depth = None
#
#     return {
#         "unprocessed_dataset": user_experiment_unprocessed_dataset,
#         "expected_output": test_data,
#     }
