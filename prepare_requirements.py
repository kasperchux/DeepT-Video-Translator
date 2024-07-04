def prepare_requirements(input_file, output_file):
  with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
    for line in f_in:
      equal_index = line.find('=')
      if equal_index != -1:
        new_line = line[:equal_index]
        f_out.write(new_line + '\n') 
      else:
        f_out.write(line + '\n')  


if __name__ == '__main__':
    prepare_requirements(r"D:\Coding\Work\DeepT\DeepT-Video-Translator\requirements.txt", r"D:\Coding\Work\DeepT\DeepT-Video-Translator\requirements_ready.txt")
