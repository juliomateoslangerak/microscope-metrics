def get_norm_intensity_matrix(img):
    """
    get normalized intensity matrix: divide all the pixels' intensity
    by the maximum intensity.
    Parameters
    ----------
    img : np.array
        image on a 2d np.array format.
    Returns
    -------
    norm_intensity_profile : np.array
        2d np.array where pixel values are scaled by the max intensity of
        the original image.
    """

    max_intensity = np.max(img)
    # the rule of three : max_intensity->100%, pixel_intensity*100/max
    norm_intensity_profile = np.round(img / max_intensity * 100)
    return DataFrame(norm_intensity_profile)


def get_max_intensity_region_table(img):
    """
    this function finds the max intensity area of the given image
    in order to figure out the number of pixels,the center of mass and
    the max intensity of the corresponding area.
    Parameters
    ----------
    img : np.array.
        2d np.array.
    Returns
    -------
    center_of_mass: dict
        dict encolsing the number of pixels, the coordinates of the
        center of mass of the and the max intensity value of the max intensity
        area of the provided image.
    """

    max_intensity = np.max(img)

    # define the maximum intensity
    threshold_value = max_intensity - 1

    # label pixels with max intesity values: binary matrix.
    labeled_foreground = (img > threshold_value).astype(int)

    # identify the region of max intensity
    properties = regionprops(labeled_foreground, img)

    # identify the center of mass of the max intensity area
    center_of_mass = (int(properties[0].centroid[0]), int(properties[0].centroid[1]))

    # number of pixels of max intensity region
    nb_pixels = properties[0].area

    # organize info in dataframe
    max_region_info = {
        "nb pixels": [nb_pixels],
        "center of mass": [center_of_mass],
        "max intensity": [max_intensity],
    }

    return max_region_info


def get_norm_intensity_profile(img, save_path=""):
    """
    plots the normalized intensity profile of the image.
    the center of mass of the max intensity area is marked in red.
    If save_path is not empty, the generated figure will be saved as png in
    the provided path.
    Parameters
    ----------
    img : np.array
        image on a 2d np.array format.
    save_path : str, optional
        path to save the generated figure including filename.
        The default is "".
    Returns
    -------
    fig : matplotlib.figure.Figure
        returns the normalized intensity profile of the image with
        the center of mass of the max intensity area marked in red.
    """

    # normalized intensity array of the given image
    norm_intensity_profile = get_norm_intensity_matrix(img)
    # coordinates of center of mass of mac intensity area
    x_mass, y_mass = get_max_intensity_region_table(img)["center of mass"][0]

    # figure construction
    fig, ax = plt.subplots()
    ax.scatter(y_mass, x_mass, s=60, color="r", marker="+")
    plt.imshow(norm_intensity_profile)
    plt.colorbar()
    plt.title("normalized intensity profile", figure=fig)
    if save_path:
        plt.savefig(str(save_path), bbox_inches="tight")

    return fig
