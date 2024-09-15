import subprocess

# 定义命令
command = 'echo 1 | bash <(curl -L -s https://raw.githubusercontent.com/lmc999/RegionRestrictionCheck/main/check.sh) -M 4'

# 运行命令并获取输出
result = subprocess.run(command, shell=True, text=True, capture_output=True)

# 获取标准输出和标准错误输出
output = result.stdout
error = result.stderr

# 将输出保存到文件
with open('output.txt', 'w') as file:
    file.write('Standard Output:\n')
    file.write(output)

print('命令输出已保存到 output.txt')