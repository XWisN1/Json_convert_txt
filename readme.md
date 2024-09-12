使用方法：

运行脚本后会在脚本所在路径创建_txt文件夹，内容都会保存到这里面
python convert_b.py key
python convert_b.py key1 key2 key3
python convert_b.py key --path D:\file_path\
python convert_b.py domain md5 sha256 --path D:\file_path\
python convert_b.py domain md5 sha256 --path D:\file_path\ --max_rows_per_file 1000

默认设置：txt最大为5000行，如果超过这个限制，会自动创建新的文件
