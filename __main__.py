import sys
import click
import os
import shutil
import loguru as logger
import photo_sorter.photo_exif_metadata as photo_exif_metadata

# ----------------------------------------------------------------------------#
@click.group()
def cli():
    """A command line interface for photo_sorter tool."""
    pass

# ----------------------------------------------------------------------------#
@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
def show_meta_data(input_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                photo = photo_exif_metadata.PhotoExifMetadata(os.path.join(root, file))
                print(f"For file '{file}':")
                for line in str(photo).split(' | '):
                    if line:
                        print(f" * {line}")

# ----------------------------------------------------------------------------#
@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', default="./output", type=click.Path())
def sort(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                input_file = os.path.join(root, file)
                photo = photo_exif_metadata.PhotoExifMetadata(input_file)
                year, month = photo.get_photo_year_month()

                output_path = os.path.join(output_dir, year, month)
                os.makedirs(output_path, exist_ok=True)
                output_file = os.path.join(output_path, file)
                print(f"Copying {input_file} to {output_file}")
                #shutil.copy2(input_file, output_file)

# ----------------------------------------------------------------------------#
@cli.command()
def test():
    photo = photo_exif_metadata.PhotoExifMetadata("./input_clean/clean_1.jpg")
    photo.set_artist("John Doe")

    photo = photo_exif_metadata.PhotoExifMetadata("./input_clean/clean_3.jpg", auto_save=False)
    photo.set_artist("John Doe")



# ----------------------------------------------------------------------------#
if __name__=='__main__':
    cli()
