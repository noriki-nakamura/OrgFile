import pathlib
import shutil
import datetime
import os
import argparse


def organize_files_by_creation_date(target_directory: str,
                                    output_directory: str):
    target_path = pathlib.Path(target_directory)
    output_path = pathlib.Path(output_directory)

    output_path.mkdir(exist_ok=True)

    print(f"'{target_path}' にあるファイルの整理を開始します...")

    for file in target_path.iterdir():
        if not file.is_file():
            continue

        try:
            creation_timestamp = os.path.getctime(file)
            creation_date = datetime.datetime.fromtimestamp(creation_timestamp)

            date_folder_name = creation_date.strftime('%Y%m%d')

            extension = \
                file.suffix[1:].upper() if file.suffix else 'no_extension'

            destination_dir = output_path / date_folder_name / extension

            destination_dir.mkdir(parents=True, exist_ok=True)

            shutil.move(file, destination_dir / file.name)
            relative_path = destination_dir.relative_to(output_path)
            print(f"移動: {file.name} -> {relative_path}")
        except Exception as e:
            print(f"エラー: {file.name} の処理中に問題が発生しました - {e}")

    print("\nファイルの整理が完了しました。")


def parse_argument():
    parser = argparse.ArgumentParser(
        description="OrgFile: Orgnize from extension and creation time."
    )
    parser.add_argument('-s', '--src',
                        required=True,
                        help='Source directory')
    parser.add_argument('-d', '--dst',
                        required=True,
                        help='Destination directory')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_argument()

    organize_files_by_creation_date(args.src, args.dst)
