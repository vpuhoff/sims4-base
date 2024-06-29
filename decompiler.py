import shutil
import sys
import os
import time
import multiprocessing
import settings
import decompile_all_multi

def get_creator_name():
    creator_name = input("Enter your creator name: ")
    return creator_name

def get_game_folder():
    game_folder = input("Enter the path to the directory with sims.exe: ")
    return os.path.abspath(game_folder)


def move_files(src_folder, dst_folder):
    # Проверяем, существует ли исходная папка
    if not os.path.exists(src_folder):
        print(f"Source folder '{src_folder}' does not exist.")
        return

    # Проверяем, существует ли целевая папка, и создаем ее, если она не существует
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # Проходим по всем элементам в исходной папке
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)

        # Перемещаем файлы и директории
        if os.path.isdir(src_path):
            shutil.move(src_path, dst_folder)
            print(f"Moved directory: {src_path} -> {dst_folder}")
        else:
            shutil.move(src_path, dst_path)
            print(f"Moved file: {src_path} -> {dst_path}")


if __name__ == "__main__":
    curr_settings = settings.Settings()
    curr_decompiler = decompile_all_multi.SimsDecompiler()

    #creator_name = get_creator_name()
    #curr_settings.set_creator_name(creator_name)

    #game_folder = get_game_folder()
    #curr_settings.set_game_folder(game_folder)

    curr_decompiler.gameplay_folder_data = os.path.join(curr_settings.game_folder, "Data", "Simulation", "Gameplay")
    curr_decompiler.gameplay_folder_game = os.path.join(curr_settings.game_folder, "Game", "Bin", "Python")

    start_time = time.time()

    curr_decompiler.fill_queue(curr_decompiler.gameplay_folder_data)
    curr_decompiler.fill_queue(curr_decompiler.gameplay_folder_game)
    curr_decompiler.worker()

    move_files(os.path.join("EA", "core"), "Sims4_lib")
    move_files(os.path.join("EA", "generated"), "Sims4_lib")
    move_files(os.path.join("EA", "simulation"), os.path.join("Sims4_lib", "simulation"))

