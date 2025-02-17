import os
import configparser
import random
import sys
import importlib.util
import pyperclip
import pandas as pd
import time


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
    # 定义初始的INI文件结构（只包含 section 和 key，值可以不同）
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
        print("自检异常，文件树已重置")
    if not os.path.exists(MODE_DIR):
        os.makedirs(MODE_DIR)
        print("自检异常，文件树已重置")
    # 检查并创建 config.ini 文件
    if not os.path.exists(CONFIG_FILE_PATH):
        # 如果文件不存在，创建并写入初始结构和值
        config = configparser.ConfigParser()
        for section, keys in INITIAL_INI_STRUCTURE.items():
            config[section] = {key: "0" for key in keys}  # 设置初始值为 0
        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)
        print("自检异常，文件树已重置")
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
            print("自检异常值，配置文件已重置")
        else:
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
                    # 动态加载模块
                    module_path = f"mod/{module_name}.py"
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    # 调用模块中的 main 方法
                    if hasattr(module, "main"):
                        module.main()
                    else:
                        print(f"模块 {module_name} 中没有 main 方法。")
                except Exception as e:
                    print(e)
                    print(f"模块 {module_name} 不存在。")

            def list_modules():
                """列出 mod 文件夹中的所有模块"""
                modules = []
                for file in os.listdir("mod"):
                    if file.endswith(".py") and file != "__init__.py":
                        modules.append(file[:-3])  # 去掉 .py 后缀
                return modules
            # 列出所有可用模块
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)
            modules = list_modules()
            print("\n已进入自定义实验数据优化模式，请按照引导程序填写要求：")
            if config['guide']['mode2'] == "0":
                sk = input("本模式可以通过用户自定义编写的模块，执行模块中的内容生成用户所需数据。模块编写请查看官方文档。引导程序中如需中途退出，请输入quit"
                           "，则会自动返回主菜单（如需后续跳过本介绍语请输入skip，无需跳过则回车）")
                if sk.lower() == "skip":
                    config['guide']['mode2'] = "1"
                with open('config/config.ini', 'w') as configfile:
                    config.write(configfile)
            print("可用模块:", modules)

            # 让用户选择模块
            module_name = input("请输入要执行的模块名: ").strip()
            if module_name in modules:
                load_and_run_module(module_name)
            else:
                print("模块不存在，请检查输入。")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')
                main()

        elif choice == "3":
            def menu():
                print("\n欢迎进入设置界面：")
                print("1. 教程重置")
                print("2. 参数调整")
                print("3. 数据统计")
                print("4. 返回主菜单")

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
            if choice == "4":
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
    print("欢迎使用提篮桥科研美容院系统（version 0.0.1）！")
    print("教程地址：https://research_modify.zhuerding.top，本程序仅用于除科研以外用途")
    print("通讯作者：有命令方块之力的附魔书，通讯地址：云南农业大学理学院，邮箱：magica_book@qq.com")
    auto_check()
    # 创建 ConfigParser 对象
    global config
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    seed()
    main()
