def prepare_requirements(input_file, output_file):
  """
  Функция, которая обрабатывает файл с зависимостями,
  удаляя все после первого знака "=" (включая сам знак)
  и добавляя символ новой строки после каждой строки.

  Args:
    input_file: Путь к файлу с зависимостями.
    output_file: Путь к файлу для сохранения результата.
  """
  with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
      # Находим первый знак "="
      equal_index = line.find('=')
      if equal_index != -1:
        # Удаляем все после первого "="
        new_line = line[:equal_index]
        f_out.write(new_line + '\n')  # Добавляем символ новой строки
      else:
        # Если знак "=" не найден, оставляем строку без изменений
        f_out.write(line + '\n')  # Добавляем символ новой строки


if __name__ == '__main__':
    prepare_requirements(r"D:\Coding\Work\DeepT\DeepT-Video-Translator\requirements.txt", r"D:\Coding\Work\DeepT\DeepT-Video-Translator\requirements_ready.txt")