import os
import configparser
import random
import sys
import importlib.util
import pyperclip
import pandas as pd
import time
import webbrowser
import requests
import hashlib
from packaging import version  # 需要安装：pip install packaging
from bs4 import BeautifulSoup


def calculate_file_hash(file_path):
    """计算文件的 MD5 哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_for_updates():
    def get_latest_version_info(url):
        """从目标网页获取最新版本号和哈希值"""
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            soup = BeautifulSoup(response.text, "html.parser")
            # 提取注释中的版本号和哈希值
            version = None
            file_hash = None
            for comment in soup.find_all(
                    string=lambda text: isinstance(text, str) and text.strip().startswith("版本号:")):
                version = comment.strip().split(":")[1].strip()
            for comment in soup.find_all(
                    string=lambda text: isinstance(text, str) and text.strip().startswith("哈希值:")):
                file_hash = comment.strip().split(":")[1].strip()
            return version, file_hash
        except Exception as e:
            print(f"获取最新版本信息失败: {e}")
            return None, None
    """检查更新"""
    # 目标网页 URL
    update_url = "https://cosmetology.zhuerding.top/version.html"

    # 获取最新版本信息
    print("[检查更新]")
    print("请保持网络畅通")
    latest_version, latest_hash = get_latest_version_info(update_url)
    if not latest_version or not latest_hash:
        print("无法获取更新信息，请检查网络连接情况。")
        return

    # 比较版本号
    if version.parse(latest_version) > version.parse(CURRENT_VERSION):
        print(f"发现新版本: {latest_version}（当前版本: {CURRENT_VERSION}）")
        # 比较哈希值
        if latest_hash != CURRENT_HASH:
            print("程序文件已更新，请访问https://github.com/zhuerding/folk_data/releases下载最新版本。")
        else:
            print("版本号已更新，但文件未更改。")
    else:
        print("更新检查结束，当前已是最新版本。")


def money():
    numby = input("实验花费：（请输入一个正实数）")
    if numby.replace(".", "", 1).isdigit():  # 检查输入是否为数字
        config["used"]["money"] = str(float(config["used"]["money"] + numby))
        with open('config/config.ini', 'w') as configfile:
            config.write(configfile)
    elif numby.lower() == "quit":  # 如果输入为"skip"，跳出当前循环
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    else:
        print("请输入一个有效的数字！")


def main_menu():
    df = pd.DataFrame()
    print("欢迎进入优化模式选择界面：")
    print("1. 单组数据优化模式")
    print("2. 自定义实验数据优化模式")
    print("3. 设置")
    print("4. 退出")

    choice = input("请输入您的选择（1/2/3/4）：")
    return choice


# 程序自检函数
def auto_check():
    print("\n程序自检中，请稍后")
    # 检查更新中
    check_for_updates()
    # 定义初始的INI文件结构（只包含 section 和 key，值可以不同）
    print("[文件完整性检查]")
    INITIAL_INI_STRUCTURE = {
        "guide": ["mode1", "mode2"],
        "set_up": ["accuracy", "float", "seed"],
        "used": ["num", "money"]
    }

    # 定义文件夹和文件路径
    CONFIG_DIR = 'config'
    MODE_DIR = 'mod'
    CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'config.ini')
    # 检查并创建 config 和 mod 文件夹
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        print("文件完整性异常，文件树已重置")
    if not os.path.exists(MODE_DIR):
        os.makedirs(MODE_DIR)
        print("文件完整性异常，文件树已重置")
    # 检查并创建 config.ini 文件
    if not os.path.exists(CONFIG_FILE_PATH):
        # 如果文件不存在，创建并写入初始结构和值
        config = configparser.ConfigParser()
        for section, keys in INITIAL_INI_STRUCTURE.items():
            config[section] = {key: "0" for key in keys}  # 设置初始值为 0
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)
        print("文件完整性异常，文件树已重置")
    else:
        # 如果文件存在，检查结构是否一致
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)

        is_consistent = True
        for section, keys in INITIAL_INI_STRUCTURE.items():
            if section not in config:
                is_consistent = False
                break
            for key in keys:
                if key not in config[section]:
                    is_consistent = False
                    break

        if not is_consistent:
            # 如果结构不一致，重置为初始结构和值
            config = configparser.ConfigParser()
            for section, keys in INITIAL_INI_STRUCTURE.items():
                config[section] = {key: "0" for key in keys}  # 设置初始值为 0
            with open(CONFIG_FILE_PATH, 'w') as configfile:
                config.write(configfile)
            print("配置文件出现异常值，配置文件已重置")
        else:
            print("文件完整性检查结束")
            print("自检结束，程序无误\n")
            config['used']['num'] = str(int(config['used']['num']) + 1)
            if 0 < int(config['used']['num']) <= 10:
                prompt = "欢迎您，学术星云！"
            elif 10 < int(config['used']['num']) <= 20:
                prompt = "您真是科研界一颗冉冉升起的主序星。"
            elif 20 < int(config['used']['num']) <= 30:
                prompt = "您就是科研界一颗熊熊燃烧的亚巨星。"
            elif 30 < int(config['used']['num']) <= 40:
                prompt = "您即是科研界一颗光芒万丈的亮巨星。"
            elif 40 < int(config['used']['num']) <= 50:
                prompt = "您定是科研界一颗无可取代的超巨星。"
            else:
                prompt = "您……已经无敌了，绝对是学术黑洞啊"
            print(f"这是您第{int(config['used']['num'])}次使用本程序,", prompt)
            if float(config['used']['num']) == 0:
                coin = "终于等到您，快来给老板省钱"
            elif 0 < float(config['used']['num']) <= 5000:
                coin = "快给老板狠狠省钱！"
            elif 5000 < float(config['used']['num']) <= 20000:
                coin = "您已经给老板节省了10瓶胎牛血清！"
            elif 20000 < float(config['used']['num']) <= 100000:
                coin = "再努努力就省出一个省自然基金啦！"
            elif 100000 < float(config['used']['num']) <= 200000:
                coin = "您已经给老板省出来一辆新车嘞！"
            elif 200000 < float(config['used']['num']) <= 500000:
                coin = "再努努力就省出一个国自然面上啦！"
            else:
                coin = "您就是老板的左膀右臂，省钱巨星！"
            print(f"您已经帮老板节省了{float(config['used']['money'])}元的科研经费，", coin)
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)


# 设置随机数种子
def seed():
    # 读取配置文件
    config.read('config/config.ini')
    if int(config["set_up"]["seed"]) == 0:
        # 设置随机数种子为当前时间种子
        random.seed(time.time())
        print("随机数种子加载完毕，目前为时间种子模式\n")


# 检验输入有效性
def get_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.replace(".", "", 1).isdigit():  # 检查输入是否为数字
            return float(user_input)
        elif user_input.lower() == "quit":  # 如果输入为"skip"，跳出当前循环
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
        else:
            print("请输入一个有效的数字！")


# 主程序
def main():
    global config
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    while True:
        choice = main_menu()
        if config['used']['num'] == "1" or config['used']['num'] == "0":
            config['set_up']['float'] = "0.05"
            config['set_up']['accuracy'] = "2"
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)
        # 选择模式
        if choice == '1':
            if config['used']['num'] == "1" or config['used']['num'] == "0":
                decimal_places = 2
                float_places = 0.05
            else:
                decimal_places = int(config['set_up']['accuracy'])
                float_places = float(config['set_up']['float'])
            print("\n已进入单组数据优化模式，请按照引导程序填写要求：")
            print(f"您当前数据精度为：{config['set_up']['accuracy']}，混淆参数为：",
                  "{:.2f}%".format(float(config['set_up']['float']) * 100), "，如有需要请前往设置界面修改。")
            if config['guide']['mode1'] == "0":
                sk = input("\n介绍：本模式为根据指定平均数和方差生成一组3个的随机数以供优化数据，请按照以下引导程序进行操作，结果自动复制到您的剪切板。引导程序中如需中途退出，请输入quit"
                           "，则会自动返回主菜单（如需后续跳过本介绍语请输入skip，无需跳过则回车）")
                if sk.lower() == "skip":
                    config['guide']['mode1'] = "1"
                    with open('config/config.ini', 'w') as configfile:
                        config.write(configfile)
                elif sk.lower() == "quit":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    main()
            # 获取平均值和标准差
            os.system('cls' if os.name == 'nt' else 'clear')
            mean = get_input("\n请输入所需数组的平均值：")
            sd = get_input("请输入所需数组的标准差：")
            # 对平均值和标准差进行偏差优化
            mean = random.uniform(mean - mean * float_places, mean + mean * float_places)
            sd = random.uniform(sd - sd * float_places, sd + sd * float_places)
            # 生成随机数
            random_numbers = [abs(round(random.gauss(mean, sd), decimal_places)) for _ in range(3)]
            # 复制随机数到剪贴板
            random_numbers_str = '\t'.join(map(str, random_numbers))
            pyperclip.copy(random_numbers_str)
            print("\n你已生成的三个随机数以tab键分割，并已复制到剪贴板，您可直接复制到excel表格中")
            print(f"您优化后的数据为:  {random_numbers_str}")
            context = input("回车后退回程序主界面")
            if context.lower() == "-m":
                money()
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
        elif choice == '2':
            def load_and_run_module(module_name):
                try:
                    # 构造模块文件路径
                    module_path = os.path.join("mod", module_name, module_name + ".py")
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    if spec is None:
                        raise ImportError(f"无法加载模块 {module_name}，文件路径 {module_path} 不存在。")
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    # 调用模块中的 main 方法
                    if hasattr(module, "main"):
                        module.main()
                    else:
                        print(f"模块 {module_name} 中没有 main 方法。")
                except ImportError:
                    print(f"模块 {module_name} 不存在。")

            def list_modules():
                """列出 mod 文件夹及其子文件夹中与子文件夹同名的模块"""
                modules = []
                for dir_name in os.listdir("mod"):
                    dir_path = os.path.join("mod", dir_name)
                    # 检查是否是文件夹
                    if os.path.isdir(dir_path):
                        # 构造与子文件夹同名的 .py 文件路径
                        module_file = os.path.join(dir_path, f"{dir_name}.py")
                        if os.path.exists(module_file):
                            # 如果存在同名 .py 文件，则将其纳入模块列表
                            # 将路径转换为模块格式（例如：subfolder1.subfolder1）
                            module_path = os.path.relpath(dir_path, "mod").replace(os.sep, '.')
                            modules.append(module_path)
                return modules
            # 列出所有可用模块
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)
            modules = list_modules()
            if not modules:
                print("未找到任何可用模块。")
                os.system('cls' if os.name == 'nt' else 'clear')
                main()
            print("\n已进入自定义实验数据优化模式，请按照引导程序填写要求：")
            if config['guide']['mode2'] == "0":
                sk = input("本模式可以通过用户自定义编写的模块，执行模块中的内容生成用户所需数据。模块编写请查看官方文档。引导程序中如需中途退出，请输入quit"
                           "，则会自动返回主菜单（如需后续跳过本介绍语请输入skip，无需跳过则回车）")
                if sk.lower() == "skip":
                    config['guide']['mode2'] = "1"
                with open('config/config.ini', 'w') as configfile:
                    config.write(configfile)
            print("可用模块:")
            for i, module in enumerate(modules, 1):
                print(f"{i}. {module}")

                # 用户选择模块
                try:
                    choice = int(input("请选择要运行的模块编号（输入 0 退出）: "))
                    if choice == 0:
                        print("退出程序。")
                        return
                    if choice < 1 or choice > len(modules):
                        print("无效的选择。")
                        return
                    selected_module = modules[choice - 1]
                    print(f"正在加载并运行模块: {selected_module}")
                    load_and_run_module(selected_module)
                except ValueError:
                    print("请输入有效的数字。")

        elif choice == "3":
            def menu():
                print("\n欢迎进入设置界面：")
                print("1. 教程重置")
                print("2. 参数调整")
                print("3. 数据统计")
                print("4. 访问教程")
                print("5. 返回主菜单")

                choice = input("请输入您的选择（1/2/3）：")
                return choice
            choice = menu()
            if choice == "1":
                a = input("\n已进入教程重置设置，如需在下一次进入时重新观看教程请输入0，返回请输入1：")
                if a == "0":
                    config["guide"]["mode1"] = "0"
                    config["guide"]["mode2"] = "0"
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    main()
            if choice == "2":
                print("\n已进入参数设置，请输入代码修改指定参数：")
                print("1. 数据精度（生成数据保留小数点后几位，请输入≥0的整数）")
                print("2. 混淆参数（输入数据在乘以±（1+混淆参数）后再以此为标准进行生成，请输入0~1的小数）")
                print("3. 返回主菜单")
                a = input("请输入参数：")
                if a == "1":
                    config["set_up"]["accuracy"] = input("请输入数据精度值（请输入≥0的整数）：")
                elif a == "2":
                    config["set_up"]["float"] = input("请输入混淆参数（请输入0~1的小数）：")
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    main()
            if choice == "3":
                print("\n以下为您使用以来的数据统计：")
                config['used']['num'] = str(int(config['used']['num']) + 1)
                if 0 < int(config['used']['num']) <= 10:
                    prompt = "欢迎您，学术星云！"
                elif 10 < int(config['used']['num']) <= 20:
                    prompt = "您真是科研界一颗冉冉升起的主序星。"
                elif 20 < int(config['used']['num']) <= 30:
                    prompt = "您就是科研界一颗熊熊燃烧的亚巨星。"
                elif 30 < int(config['used']['num']) <= 40:
                    prompt = "您即是科研界一颗光芒万丈的亮巨星。"
                elif 40 < int(config['used']['num']) <= 50:
                    prompt = "您定是科研界一颗无可取代的超巨星。"
                else:
                    prompt = "您……已经无敌了，绝对是学术黑洞啊"
                print(f"这是您第{int(config['used']['num'])}次使用本程序,", prompt)
                if float(config['used']['num']) == 0:
                    coin = "终于等到您，快来给老板省钱"
                elif 0 < float(config['used']['num']) <= 5000:
                    coin = "快给老板狠狠省钱！"
                elif 5000 < float(config['used']['num']) <= 20000:
                    coin = "您已经给老板节省了10瓶胎牛血清！"
                elif 20000 < float(config['used']['num']) <= 100000:
                    coin = "再努努力就省出一个省自然基金啦！"
                elif 100000 < float(config['used']['num']) <= 200000:
                    coin = "您已经给老板省出来一辆新车嘞！"
                elif 200000 < float(config['used']['num']) <= 500000:
                    coin = "再努努力就省出一个国自然面上啦！"
                else:
                    coin = "您就是老板的左膀右臂，省钱巨星！"
                print(f"您已经帮老板节省了{float(config['used']['money'])}元的科研经费，", coin)
                sk = input("回车返回主菜单，如需重置请输入reset")
                if sk.lower() == "reset":
                    echo = input("您确定重置吗？（yes/no）")
                    if echo.lower() == "yes":
                        config['used']['num'] = "0"
                        config['used']['money'] = "0"
                        with open('config/config.ini', 'w') as configfile:
                            config.write(configfile)
                os.system('cls' if os.name == 'nt' else 'clear')
                main()
            elif choice == '4':
                webbrowser.open("https://cosmetology.zhuerding.top/")
            elif choice == "5":
                os.system('cls' if os.name == 'nt' else 'clear')
                main()
        elif choice == '4':
            print("感谢您的使用，已退出程序！")
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)
            sys.exit()
        else:
            print("无效的选择，请重新输入！")
            main()


if __name__ == "__main__":
    # 程序当前版本号和哈希值
    CURRENT_VERSION = "0.0.2"
    current_file_hash = calculate_file_hash(__file__)
    # print(f"当前文件哈希值: {current_file_hash}")
    CURRENT_HASH = "103cc20eccdbb7e13dc61afa53b50aa3"  # 示例哈希值，需根据实际文件计算
    print("欢迎使用提篮桥科研美容院系统（version 0.0.2）！")
    print("教程地址：https://cosmetology.zhuerding.top/，本程序仅用于除科研以外用途")
    print("通讯作者：有命令方块之力的附魔书，通讯地址：云北工农兵大学黄埔学院，邮箱：magica_book@qq.com")
    auto_check()
    # 创建 ConfigParser 对象
    global config
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    if config["used"]["num"] == str(1):
        webbrowser.open("https://cosmetology.zhuerding.top/")
    seed()
    main()
