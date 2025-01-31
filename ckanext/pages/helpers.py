import os
from werkzeug.utils import secure_filename
from ckan.common import config


def _validate_image_upload(file_storage):
    """Validate that the uploaded file is an image."""
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    if not file_storage:
        raise ValidationError({'logo': _('No file uploaded')})

    filename = secure_filename(file_storage.filename)
    if not filename:
        raise ValidationError({'logo': _('Invalid filename')})

    file_ext = filename.rsplit('.', 1)[1].lower()
    if file_ext not in allowed_extensions:
        raise ValidationError({'logo': _('File type not allowed. Only images are allowed.')})

    return filename


def _save_image(file_storage, filename):
    """Save the uploaded image to the configured upload directory."""
    upload_path = config.get('ckan.storage_path', '/var/lib/ckan/storage')
    logo_path = os.path.join(upload_path, 'header_logos')

    if not os.path.exists(logo_path):
        os.makedirs(logo_path)

    file_path = os.path.join(logo_path, filename)
    file_storage.save(file_path)

    return file_path