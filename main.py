import zipfile, os, hashlib, re, requests, csv

# Задание 1
os.mkdir('./result_dir')
directory_to_extract_to = './result_dir'
arch_file = zipfile.ZipFile('./tiff-4.2.0_lab1.zip')
arch_file.extractall(directory_to_extract_to)
arch_file.close()

# Задание 2
print("Все тхт файлы:")
for root, directories, files in os.walk(directory_to_extract_to):
    for file in files:
        if ".txt" in file:
            f = open(os.path.join(root, file), 'rb').read()
            print(os.path.join(root, file) + ' Hash: ' + hashlib.md5(f).hexdigest())

# Задание 3
print("Путь файла с указанным хэшем")
link = ''
for root, directories, files in os.walk(directory_to_extract_to):
    for file in files:
        f = open(os.path.join(root, file), 'rb').read()
        if hashlib.md5(f).hexdigest() == "4636f9ae9fef12ebd56cd39586d33cfb":
            print('Искомый файл: ' + os.path.join(root, file) + ' Hash: ' + hashlib.md5(f).hexdigest())
            link = f

# Задание 4
r = requests.get(link)
result_dct = {}
counter = 1
lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
headers = re.sub('<.*?>', ' ', lines[0])
headers = re.findall(r'Заболели|Умерли|Вылечились|Активные случаи', headers)

for line in lines:
    if counter > 0:
        counter = 0
        continue

    temp = re.sub('<.*?>', ';', line)
    temp = re.sub('\(.*?\)', '', temp)
    temp = re.sub(';+', ';', temp)
    temp = temp[1: len(temp) - 1]
    temp = re.sub('\s(?=\d)', '', temp)
    temp = re.sub('(?<=\d)\s', '', temp)
    temp = re.sub('(?<=0)\*', '', temp)
    temp = re.sub('_', '-1', temp)

    result = temp.split(';')
    if len(result) == 6:
        result.pop(0)

    country_name = result[0]
    country_name = re.sub('.*\s\s', '', country_name)

    result_dct[country_name] = [0, 0, 0, 0]
    result_dct[country_name][0] = result[1]
    result_dct[country_name][1] = result[2]
    result_dct[country_name][2] = result[3]
    result_dct[country_name][3] = result[4]

# Задание 5
output = open('data.csv', 'w', encoding='utf-16')
writer = csv.writer(output)

for key, value in result_dct.items():
    writer.writerow([key, value])
output.close()

# Задание 6
target_country = input("Введите название страны: ")
print(result_dct[target_country])
