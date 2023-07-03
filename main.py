import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from googletrans import Translator
import re
import os
import time

def translate_lua_config_file(lua_filepath, output_dir, target_languages, progress_bar, progress_label):
    translator = Translator(service_urls=["translate.google.com"])
    label_pattern = re.compile(r"\['label'\]\s*=\s*'([^']*)'")
    description_pattern = re.compile(r"\['description'\]\s*=\s*'([^']*)'")

    with open(lua_filepath, 'r', encoding='utf-8') as lua_file:
        lines = lua_file.readlines()

    num_languages = len(target_languages)
    progress_per_lang = 100 / num_languages

    start_time = time.time()
    previous_time = start_time

    error_log = []  # List to store error logs

    for i, lang in enumerate(target_languages, start=1):
        translated_lua_filepath = os.path.join(output_dir, f"translated_config_{lang}.lua")

        with open(translated_lua_filepath, 'w', encoding='utf-8') as output_file:
            labels_translated = 0

            for j, line in enumerate(lines, start=1):
                try:
                    label_match = label_pattern.search(line)
                    description_match = description_pattern.search(line)

                    if label_match:
                        english_label = label_match.group(1)
                        if english_label:
                            retry = True
                            while retry:
                                try:
                                    translated_label = translator.translate(english_label, src='en', dest=lang).text
                                    translated_label = translated_label.replace("'", "\\'")  # check for single quotes and add \
                                    line = line.replace(english_label, translated_label)
                                    labels_translated += 1
                                    retry = False
                                except Exception as e:
                                    error_log.append(f"Error occurred while translating line {j}: Label: {line.strip()}")
                                    break

                    if description_match:
                        english_description = description_match.group(1)
                        if english_description:
                            retry = True
                            while retry:
                                try:
                                    translated_description = translator.translate(english_description, src='en', dest=lang).text
                                    translated_description = translated_description.replace("'", "\\'")  # same as above
                                    line = line.replace(english_description, translated_description)
                                    retry = False
                                except Exception as e:
                                    error_log.append(f"Error occurred while translating line {j}: Description: {line.strip()}")
                                    break

                    output_file.write(line)
                except Exception as e:
                    error_log.append(f"Error occurred while translating line {j}: {str(e)}")

                
                current_progress = (i - 1) * progress_per_lang + (j / len(lines)) * progress_per_lang
                progress_bar["value"] = current_progress
                progress_bar.update()

                
                current_time = time.time()
                elapsed_time = current_time - start_time
                iterations_done = (i - 1) * len(lines) + j
                total_iterations = num_languages * len(lines)
                remaining_iterations = total_iterations - iterations_done
                remaining_time = (remaining_iterations * elapsed_time) / iterations_done

                
                progress_text = f"Approximately remaining time: {remaining_time / 60:.2f} minutes"
                progress_label["text"] = progress_text

                
                if current_time - previous_time >= 0.5:
                    progress_bar.update()
                    previous_time = current_time

        # Some debug print(f"Translation to {lang} completed. Translated file: {translated_lua_filepath}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    time_comment = f"\n--[[ Kyle's Translator\n\nThanks for using my script\n\nTranslation Time: {elapsed_time / 60:.2f} minutes\nLabels translated: {labels_translated}\nDescriptions translated: {labels_translated * num_languages}\n\nMy discord: kyle337\n\n--]]\n"
    with open(translated_lua_filepath, 'a', encoding='utf-8') as output_file:
        output_file.write(time_comment)

    # Save error log to a file
    error_log_filepath = os.path.join(output_dir, "things_to_manually_do.txt")
    with open(error_log_filepath, 'w') as error_log_file:
        error_log_file.write("\n".join(error_log))

def select_files_and_translate():
    root = tk.Tk()
    root.withdraw()

    initial_dir = os.path.dirname(os.path.realpath(__file__))

    lua_filepath = filedialog.askopenfilename(initialdir=initial_dir, title="Select Item File")
    if not lua_filepath:
        print("No Item file selected.")
        return

    output_dir = os.path.join(initial_dir, "translations")
    os.makedirs(output_dir, exist_ok=True)

    target_languages = ['it']  # here you put your language, check the languages.txt file to find your lang code!

    # Create the progress bar and label
    progress_window = tk.Toplevel()
    progress_window.title("Progress")

    progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate", maximum=100)
    progress_bar.pack(padx=10, pady=10)

    progress_label = tk.Label(progress_window, text="Remaining time: ...")
    progress_label.pack(padx=10, pady=5)

    translate_lua_config_file(lua_filepath, output_dir, target_languages, progress_bar, progress_label)

    # Close progress window
    progress_window.destroy()

select_files_and_translate()
