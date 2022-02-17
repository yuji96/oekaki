from pathlib import Path

import numpy as np
from PIL import Image


def convert_to_ndarray(fig):
    fig.canvas.draw()
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    w, h = fig.canvas.get_width_height()
    return data.reshape((h, w, 3))


def save_diff_image(expected_image, actual_image, output):
    expected_image = np.array(expected_image).astype(float)
    actual_image = np.array(actual_image).astype(float)
    abs_diff_image = np.abs(expected_image - actual_image)

    # expand differences in luminance domain
    abs_diff_image *= 255 * 10
    save_image_np = np.clip(abs_diff_image, 0, 255).astype(np.uint8)
    height, width, depth = save_image_np.shape

    # The PDF renderer doesn't produce an alpha channel, but the
    # matplotlib PNG writer requires one, so expand the array
    if depth == 3:
        with_alpha = np.empty((height, width, 4), dtype=np.uint8)
        with_alpha[:, :, 0:3] = save_image_np
        save_image_np = with_alpha

    # Hard-code the alpha channel to fully solid
    save_image_np[:, :, 3] = 255

    path = Path(output).parent
    if not path.exists():
        path.mkdir(parents=True)
    Image.fromarray(save_image_np).save(output, format="png")
