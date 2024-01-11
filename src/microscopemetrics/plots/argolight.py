import matplotlib.pyplot as plt
import numpy as np

from microscopemetrics.plots import Reporter


class ArgolightReporter(Reporter):
    """Reporter subclass to produce Argolight sample figures"""

    def __init__(self):
        image_report_to_func = {
            "spots": self.full_report_spots,
            "vertical_resolution": self.full_report_vertical_resolution,
            "horizontal_resolution": self.full_report_horizontal_resolution,
        }

        super().__init__(image_report_to_func=image_report_to_func)

    def produce_image_report(self, image):
        pass

    def full_report_spots(self, image):
        pass

    def full_report_vertical_resolution(self, image):
        pass

    def full_report_horizontal_resolution(self, image):
        pass

    def plot_homogeneity_map(self, image):
        nr_channels = image.getSizeC()
        x_dim = image.getSizeX()
        y_dim = image.getSizeY()

        tables = self.get_tables(image, namespace_start="metrics", name_filter="properties")
        if len(tables) != 1:
            raise Exception(
                "There are none or more than one properties tables. Verify data integrity."
            )
        table = tables[0]

        row_count = table.getNumberOfRows()
        col_names = [c.name for c in table.getHeaders()]
        wanted_columns = [
            "channel",
            "max_intensity",
            "mean_intensity",
            "integrated_intensity",
            "x_weighted_centroid",
            "y_weighted_centroid",
        ]

        fig, axes = plt.subplots(
            ncols=nr_channels, nrows=3, squeeze=False, figsize=(3 * nr_channels, 9)
        )

        for ch in range(nr_channels):
            data = table.slice(
                [col_names.index(w_col) for w_col in wanted_columns],
                table.getWhereList(
                    condition=f"channel=={ch}",
                    variables={},
                    start=0,
                    stop=row_count,
                    step=0,
                ),
            )
            max_intensity = np.array(
                [val for col in data.columns for val in col.values if col.name == "max_intensity"]
            )
            integrated_intensity = np.array(
                [
                    val
                    for col in data.columns
                    for val in col.values
                    if col.name == "integrated_intensity"
                ]
            )
            x_positions = np.array(
                [
                    val
                    for col in data.columns
                    for val in col.values
                    if col.name == "x_weighted_centroid"
                ]
            )
            y_positions = np.array(
                [
                    val
                    for col in data.columns
                    for val in col.values
                    if col.name == "y_weighted_centroid"
                ]
            )
            grid_x, grid_y = np.mgrid[0:x_dim, 0:y_dim]
            image_intensities = get_intensities(image, c_range=ch, t_range=0).max(0)

            try:
                interpolated_max_int = griddata(
                    np.stack((x_positions, y_positions), axis=1),
                    max_intensity,
                    (grid_x, grid_y),
                    method="linear",
                )
                interpolated_intgr_int = griddata(
                    np.stack((x_positions, y_positions), axis=1),
                    integrated_intensity,
                    (grid_x, grid_y),
                    method="linear",
                )
            except Exception as e:
                # TODO: Log a warning
                interpolated_max_int = np.zeros((256, 256))

            ax = axes.ravel()
            ax[ch] = plt.subplot(3, 4, ch + 1)

            ax[ch].imshow(np.squeeze(image_intensities), cmap="gray")
            ax[ch].set_title("MIP_" + str(ch))

            ax[ch + nr_channels].imshow(
                np.flipud(interpolated_intgr_int),
                extent=(0, x_dim, y_dim, 0),
                origin="lower",
                cmap=cm.hot,
                vmin=np.amin(integrated_intensity),
                vmax=np.amax(integrated_intensity),
            )
            ax[ch + nr_channels].plot(x_positions, y_positions, "k.", ms=2)
            ax[ch + nr_channels].set_title("Integrated_int_" + str(ch))

            ax[ch + 2 * nr_channels].imshow(
                np.flipud(interpolated_max_int),
                extent=(0, x_dim, y_dim, 0),
                origin="lower",
                cmap=cm.hot,
                vmin=np.amin(image_intensities),
                vmax=np.amax(image_intensities),
            )
            ax[ch + 2 * nr_channels].plot(x_positions, y_positions, "k.", ms=2)
            ax[ch + 2 * nr_channels].set_title("Max_int_" + str(ch))

        plt.show()

    def plot_distances_map(self, image):
        nr_channels = image.getSizeC()
        x_dim = image.getSizeX()
        y_dim = image.getSizeY()

        tables = get_tables(image, namespace_start="metrics", name_filter="distances")
        if len(tables) != 1:
            raise Exception(
                "There are none or more than one distances tables. Verify data integrity."
            )
        table = tables[0]
        row_count = table.getNumberOfRows()
        col_names = [c.name for c in table.getHeaders()]

        # We need the positions too
        pos_tables = get_tables(image, namespace_start="metrics", name_filter="properties")
        if len(tables) != 1:
            raise Exception(
                "There are none or more than one positions tables. Verify data integrity."
            )
        pos_table = pos_tables[0]
        pos_row_count = pos_table.getNumberOfRows()
        pos_col_names = [c.name for c in pos_table.getHeaders()]

        fig, axes = plt.subplots(
            ncols=nr_channels - 1,
            nrows=nr_channels,
            squeeze=False,
            figsize=((nr_channels - 1) * 3, nr_channels * 3),
        )

        ax_index = 0
        for ch_A in range(nr_channels):
            pos_data = pos_table.slice(
                [
                    pos_col_names.index(w_col)
                    for w_col in [
                        "channel",
                        "mask_labels",
                        "x_weighted_centroid",
                        "y_weighted_centroid",
                    ]
                ],
                pos_table.getWhereList(
                    condition=f"channel=={ch_A}",
                    variables={},
                    start=0,
                    stop=pos_row_count,
                    step=0,
                ),
            )

            mask_labels = np.array(
                [val for col in pos_data.columns for val in col.values if col.name == "mask_labels"]
            )
            x_positions = np.array(
                [
                    val
                    for col in pos_data.columns
                    for val in col.values
                    if col.name == "x_weighted_centroid"
                ]
            )
            y_positions = np.array(
                [
                    val
                    for col in pos_data.columns
                    for val in col.values
                    if col.name == "y_weighted_centroid"
                ]
            )
            positions_map = np.stack((x_positions, y_positions), axis=1)

            for ch_B in [i for i in range(nr_channels) if i != ch_A]:
                data = table.slice(
                    list(range(len(col_names))),
                    table.getWhereList(
                        condition=f"(channel_A=={ch_A})&(channel_B=={ch_B})",
                        variables={},
                        start=0,
                        stop=row_count,
                        step=0,
                    ),
                )
                labels_map = np.array(
                    [
                        val
                        for col in data.columns
                        for val in col.values
                        if col.name == "ch_A_roi_labels"
                    ]
                )
                labels_map += 1  # Mask labels are augmented by one as 0 is background
                distances_map_3d = np.array(
                    [val for col in data.columns for val in col.values if col.name == "distance_3d"]
                )
                distances_map_x = np.array(
                    [val for col in data.columns for val in col.values if col.name == "distance_x"]
                )
                distances_map_y = np.array(
                    [val for col in data.columns for val in col.values if col.name == "distance_y"]
                )
                distances_map_z = np.array(
                    [val for col in data.columns for val in col.values if col.name == "distance_z"]
                )

                filtered_positions = positions_map[
                    np.intersect1d(
                        mask_labels, labels_map, assume_unique=True, return_indices=True
                    )[1],
                    :,
                ]

                grid_x, grid_y = np.mgrid[0:x_dim:1, 0:y_dim:1]
                interpolated = griddata(
                    filtered_positions,
                    distances_map_3d,
                    (grid_x, grid_y),
                    method="cubic",
                )

                ax = axes.ravel()
                ax[ax_index].imshow(
                    np.flipud(interpolated),
                    extent=(0, x_dim, y_dim, 0),
                    origin="lower",
                    cmap=cm.hot,
                    vmin=np.amin(distances_map_3d),
                    vmax=np.amax(distances_map_3d),
                )
                ax[ax_index].set_title(f"Distance Ch{ch_A}-Ch{ch_B}")

                ax_index += 1

        plt.show()
