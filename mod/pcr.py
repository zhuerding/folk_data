import configparser
import os
import webbrowser

import pandas as pd
from datetime import datetime
import random
import sys


def get_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.replace(".", "", 1).isdigit():  # 检查输入是否为数字
            return float(user_input)
        elif user_input.lower() == "quit":
            load_main_from_exe()
        else:
            print("请输入一个有效的数字！")
            

# 动态导入 index.exe 中的 main 函数
def load_main_from_exe():
    # 获取 index.exe 的路径
    exe_dir = os.path.dirname(sys.executable)  # 获取 index.exe 所在的目录
    sys.path.append(exe_dir)  # 将 index.exe 所在目录添加到 Python 路径

    # 动态导入 index 模块
    import index
    os.system('cls' if os.name == 'nt' else 'clear')
    index.main()  # 调用 main 函数


def main():
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('config/config.ini')
    if config['used']['num'] == "1" or config['used']['num'] == "0":
        config['set_up']['accuracy'] = "2"
        config['set_up']['float'] = "0.05"
        with open('config/config.ini', 'w') as configfile:
            config.write(configfile)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n已进入PCR数据优化模式，请按照引导程序填写要求：")
    print(f"您当前数据精度为：{config['set_up']['accuracy']}，混淆参数为：",
          "{:.2f}%".format(float(config['set_up']['float']) * 100), "，如有需要请前往设置界面修改。")
    print("本模式会根据PCR数据的模式以供优化数据，请按照以下引导程序进行操作，结果自动生成到Execl.以下为具体模式：")
    print("1. 简单优化模式")
    print("2. 倍数优化模式")
    print("3. 自定义优化模式")
    sk = input("请输入编号进入相应模式.若需要模式介绍请输入/help；如需在模式中途退出，回到主菜单请输入quit.\n")
    if sk.lower() == "quit":
        load_main_from_exe()
    elif sk.lower() == "help":
        input("\n以下为各模式介绍，敲击回车键以继续介绍……")
        input("简单优化模式：根据您指定的各组平均值和标准差优化，即仅优化△CT值，并生成△CT Mean和△CT SD")
        input("倍数优化模式：根据模板，您可以通过设置对照组△CT值平均值和内参基因CT值，随后通过百分比的方式设置其他实验组样本，即模拟真实PCR数据，一个生物学重复样本有3个CT值，最后优化△CT"
              "值，并生成△CT Mean和△CT SD。本模式相较于自定义优化模式更模式化，具体操作请查看readme.md")
        input("自定义优化模式：根据您指定的各组△CT值平均值和内参基因CT值优化，即模拟真实PCR数据，一个生物学重复样本有3个CT值，最后优化△CT值，并生成△CT Mean和△CT "
              "SD。本模式相较于详细优化模式更自由化，具体操作请查看readme.md")
        a = input("其余具体细节可访问教程：https://cosmetology.zhuerding.top/tutorial/PCR_readme.html，输入ok即可访问，回车以继续介绍")
        if a.lower() == "ok":
            webbrowser.open("https://cosmetology.zhuerding.top/tutorial/PCR_readme.html")
        print("介绍已结束")

    elif sk == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("已进入简单优化模式，请按照引导程序填写要求：")

        def generate_ct_values(mean, std, num_replicates):
            """
            根据给定的平均数和标准差生成 △CT 值
            """
            decimal_places = int(config['set_up']['accuracy'])
            return [abs(round(random.gauss(mean, std), decimal_places)) for _ in range(num_replicates)]

        def create_excel(sample_names, treatments, replicates_info, gene_name, output_file):
            """
            创建 Excel 表格
            """
            data = []
            for sample in sample_names:
                for treatment in treatments:
                    # 获取该样品和处理方式的重复实验数和平均数
                    num_replicates, mean_ct, std_ct = replicates_info[(sample, treatment)]
                    float_places = float(config['set_up']['float'])
                    decimal_places = int(config['set_up']['accuracy'])
                    # 对平均值和标准差进行偏差优化
                    mean_ct = round(random.uniform(mean_ct - mean_ct * float_places, mean_ct + mean_ct * float_places),
                                    decimal_places)
                    std_ct = round(random.uniform(std_ct - std_ct * float_places, std_ct + std_ct * float_places),
                                   decimal_places)
                    ct_values = generate_ct_values(mean_ct, std_ct, num_replicates)

                    for rep in range(num_replicates):
                        row = [
                            sample,  # 样本名
                            treatment,  # 处理方式
                            f"rep {rep + 1}",  # 重复实验编号
                            gene_name,  # 目的基因名称
                            ct_values[rep],  # △CT 值
                            mean_ct,  # 该处理方式的 △CT 值平均数
                            std_ct,  # 该处理方式的 △CT 值标准差
                        ]
                        data.append(row)
                    config["used"]["money"] = str(float(config["used"]["money"]) + 3 * 3 * 2 * num_replicates)
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)

            # 创建 DataFrame
            df = pd.DataFrame(data, columns=[
                "Sample Name", "Group", "Repeat code", f"Target", "△CT ", "△CT Mean", "△CT SD"
            ])

            # 保存为 Excel 文件
            df.to_excel(output_file, index=False)
            print(f"Excel 文件已生成: {output_file}")

        # 用户输入
        sample_names = input("请输入样本名（用英文逗号分隔）: ").strip().split(",")
        if sample_names[0].lower() == "quit":
            load_main_from_exe()
        treatments = input("请输入处理方式（用英文逗号分隔）: ").strip().split(",")
        if treatments[0].lower() == "quit":
            load_main_from_exe()
        gene_name = input("请输入目的基因名称: ")
        if gene_name.lower() == "quit":
            load_main_from_exe()
        output_file = input("请输入输出文件名（例如 output.xlsx）: ")
        if output_file.lower() == "quit":
            load_main_from_exe()

        # 获取当前日期并格式化为 YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")
        # 生成带日期的文件名
        output_file = f"{current_date}_{output_file}.xlsx"

        # 为每个样品和处理方式的组合输入重复实验数和平均数
        replicates_info = {}
        for sample in sample_names:
            for treatment in treatments:
                num_replicates = int(get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的重复实验数: "))
                mean_ct = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的 △CT 平均数: ")
                std_ct = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的 △CT 标准差: ")
                replicates_info[(sample, treatment)] = (num_replicates, mean_ct, std_ct)
        # 创建 Excel 文件
        create_excel(sample_names, treatments, replicates_info, gene_name, output_file)
    elif sk == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("已进入倍数优化模式，请按照引导程序填写要求：")

        def generate_ct_values(mean, std, num_replicates):
            """
            根据给定的平均数和标准差生成 CT 值
            """
            decimal_places = int(config['set_up']['accuracy'])
            return [round(random.gauss(mean, std), decimal_places) for _ in range(num_replicates)]

        def calculate_statistics(values):
            """
            计算一组值的平均值和标准差
            """
            decimal_places = int(config['set_up']['accuracy'])
            mean = round(sum(values) / len(values), decimal_places)
            std = round((sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5, decimal_places)
            return mean, std

        def create_excel(sample_names, treatments, replicates_info, target_gene, ref_gene, output_file):
            """
            创建 Excel 表格
            """
            data = []
            float_places = float(config['set_up']['float'])
            decimal_places = int(config['set_up']['accuracy'])
            for sample in sample_names:
                for treatment in treatments:
                    # 获取该样品和处理方式的重复实验数、△CT 值平均数及标准差、内参基因 CT 值平均数及标准差
                    num_replicates, delta_ct_mean, delta_ct_std, ref_mean, ref_std, target_ct_std = replicates_info[
                        (sample, treatment)]
                    delta_ct_mean = round(random.uniform(delta_ct_mean - delta_ct_mean * float_places,
                                                         delta_ct_mean + delta_ct_mean * float_places), decimal_places)
                    delta_ct_std = round(random.uniform(delta_ct_std - delta_ct_std * float_places,
                                                        delta_ct_std + delta_ct_std * float_places), decimal_places)
                    ref_mean = round(random.uniform(ref_mean - ref_mean * float_places * 2,
                                                    ref_mean + ref_mean * float_places * 2), decimal_places)
                    ref_std = round(random.uniform(ref_std - ref_std * float_places,
                                                   ref_std + ref_std * float_places), decimal_places)
                    target_ct_std = round(random.uniform(target_ct_std - target_ct_std * float_places,
                                                         target_ct_std + target_ct_std * float_places), decimal_places)
                    for rep in range(num_replicates):
                        # 生成该重复中的 △CT 值
                        delta_ct = round(random.gauss(delta_ct_mean, delta_ct_std), decimal_places)

                        # 生成该重复中的内参基因 CT 值（添加 ±0.05 的混淆值）
                        ref_ct_mean_rep = ref_mean
                        ref_ct_values = generate_ct_values(ref_ct_mean_rep, ref_std, 3)

                        # 计算该重复中目的基因的 CT 值
                        target_ct_mean_rep = ref_ct_mean_rep + delta_ct
                        target_ct_values = generate_ct_values(target_ct_mean_rep, target_ct_std, 3)

                        # 计算目的基因和内参基因的 CT 平均值和标准差
                        target_ct_mean, target_ct_std = calculate_statistics(target_ct_values)
                        ref_ct_mean, ref_ct_std = calculate_statistics(ref_ct_values)

                        # 添加一行数据
                        row = [
                            sample,  # 样本名
                            treatment,  # 处理方式
                            f"rep {rep + 1}",  # 重复实验编号
                            *target_ct_values,  # 目的基因 CT 值（3 个样本重复）
                            target_ct_mean,  # 目的基因 CT 平均值
                            target_ct_std,  # 目的基因 CT 标准差
                            *ref_ct_values,  # 内参基因 CT 值（3 个样本重复）
                            ref_ct_mean,  # 内参基因 CT 平均值
                            ref_ct_std,  # 内参基因 CT 标准差
                            delta_ct,  # △CT 值
                            delta_ct_mean,  # 该处理方式的 △CT 值平均数
                            delta_ct_std,  # 该处理方式的 △CT 值标准差
                        ]
                        data.append(row)
                    config["used"]["money"] = str(float(config["used"]["money"]) + 3 * 3 * 2 * num_replicates)
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)

            # 创建 DataFrame
            df = pd.DataFrame(data, columns=[
                "Sample Name", "Group", "Repeat Number",
                f"{target_gene} CT   1", f"{target_gene} CT   2", f"{target_gene} CT   3",
                f"{target_gene} CT Mean", f"{target_gene} SD",
                f"{ref_gene} CT   1", f"{ref_gene} CT   2", f"{ref_gene} CT   3", f"{ref_gene} CT Mean",
                f"{ref_gene} CT SD",
                "△CT", "△CT Mean", "△CT SD"
            ])

            # 保存为 Excel 文件
            df.to_excel(output_file, index=False)
            print(f"Excel 文件已生成: {output_file}")

        # 用户输入
        sample_names = input("请输入样本名（用逗号分隔）: ").strip().split(",")
        if sample_names[0].lower() == "quit":
            load_main_from_exe()
        target_gene = input("请输入目的基因名称: ")
        if target_gene.lower() == "quit":
            load_main_from_exe()
        ref_gene = input("请输入内参基因名称: ")
        if ref_gene.lower() == "quit":
            load_main_from_exe()
        base_filename = input("请输入文件名（无需扩展名，例如 output）: ")
        if base_filename.lower() == "quit":
            load_main_from_exe()

        # 获取当前日期并格式化为 YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")
        # 生成带日期的文件名
        output_file = f"{current_date}_{base_filename}.xlsx"

        # 固定处理方式为 sh、ov、ctrl
        treatments = ["sh", "ov", "ctrl"]

        # 为每个样本输入 ctrl 组的重复实验数、△CT 值平均数及标准差、内参基因 CT 值平均数及标准差
        replicates_info = {}
        for sample in sample_names:
            print(f"\n请输入样本 '{sample}' 的 ctrl 组数据:")
            num_replicates = input("请输入 ctrl 组的重复实验数: ")
            if num_replicates.lower() == "quit":
                load_main_from_exe()
            else:
                num_replicates = int(num_replicates)
            ctrl_delta_ct_mean = get_input("请输入 ctrl 组的 △CT 值平均数: ")
            ctrl_delta_ct_std = get_input("请输入 ctrl 组的 △CT 值标准差: ")
            ref_mean = get_input("请输入 ctrl 组的内参基因 CT 值平均数: ")
            ref_std = get_input("请输入 ctrl 组的内参基因 CT 值标准差: ")
            target_ct_std = get_input("请输入 ctrl 组的目的基因 CT 值标准差: ")

            # 导入混淆变量
            float_places = float(config['set_up']['float'])
            decimal_places = int(config['set_up']['accuracy'])
            # 为 ov 和 sh 组输入 △CT 值是 ctrl 的多少倍
            ov_multiplier = get_input("请输入 ov 组的 △CT 值是 ctrl 的多少倍: ")
            ov_multiplier = round(random.uniform(ov_multiplier - ov_multiplier * float_places,
                                 ov_multiplier + ov_multiplier * float_places), decimal_places)
            sh_multiplier = get_input("请输入 sh 组的 △CT 值是 ctrl 的多少倍: ")
            sh_multiplier = round(random.uniform(sh_multiplier - sh_multiplier * float_places,
                                                 sh_multiplier + sh_multiplier * float_places), decimal_places)

            # 计算 ov 和 sh 组的 △CT 值平均数和标准差
            ov_delta_ct_mean = ctrl_delta_ct_mean * ov_multiplier
            ov_delta_ct_std = ctrl_delta_ct_std * ov_multiplier
            sh_delta_ct_mean = ctrl_delta_ct_mean * sh_multiplier
            sh_delta_ct_std = ctrl_delta_ct_std * sh_multiplier

            # 存储每个样本和处理方式的信息
            replicates_info[(sample, "ctrl")] = (
                num_replicates, ctrl_delta_ct_mean, ctrl_delta_ct_std, ref_mean, ref_std, target_ct_std)
            replicates_info[(sample, "ov")] = (num_replicates, ov_delta_ct_mean, ov_delta_ct_std, ref_mean, ref_std, target_ct_std)
            replicates_info[(sample, "sh")] = (num_replicates, sh_delta_ct_mean, sh_delta_ct_std, ref_mean, ref_std, target_ct_std)

        # 创建 Excel 文件
        create_excel(sample_names, treatments, replicates_info, target_gene, ref_gene, output_file)
        input("回车后退回程序主界面")
        os.system('cls' if os.name == 'nt' else 'clear')
        load_main_from_exe()

    elif sk == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("已进入自定义优化模式，请按照引导程序填写要求：")

        def generate_ct_values(mean, std, num_replicates):
            """
            根据给定的平均数和标准差生成 CT 值
            """
            decimal_places = int(config['set_up']['accuracy'])
            return [round(random.gauss(mean, std), decimal_places) for _ in range(num_replicates)]

        def calculate_statistics(values):
            """
            计算一组值的平均值和标准差
            """
            decimal_places = int(config['set_up']['accuracy'])
            mean = round(sum(values) / len(values), decimal_places)
            std = round((sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5, decimal_places)
            return mean, std

        def create_excel(sample_names, treatments, replicates_info, target_gene, ref_gene, output_file):
            """
            创建 Excel 表格
            """
            data = []

            for sample in sample_names:
                for treatment in treatments:
                    # 获取该样品和处理方式的重复实验数、△CT 值平均数及标准差、内参基因 CT 值平均数及标准差
                    num_replicates, delta_ct_mean, delta_ct_std, ref_mean, ref_std, target_ct_std = replicates_info[
                        (sample, treatment)]
                    float_places = float(config['set_up']['float'])
                    decimal_places = int(config['set_up']['accuracy'])
                    delta_ct_mean = round(random.uniform(delta_ct_mean - delta_ct_mean * float_places,
                                                         delta_ct_mean + delta_ct_mean * float_places), decimal_places)
                    delta_ct_std = round(random.uniform(delta_ct_std - delta_ct_std * float_places,
                                                        delta_ct_std + delta_ct_std * float_places), decimal_places)
                    ref_mean = round(random.uniform(ref_mean - ref_mean * float_places,
                                                    ref_mean + ref_mean * float_places), decimal_places)
                    ref_std = round(random.uniform(ref_std - ref_std * float_places,
                                                   ref_std + ref_std * float_places), decimal_places)
                    target_ct_std = round(random.uniform(target_ct_std - target_ct_std * float_places,
                                                         target_ct_std + target_ct_std * float_places), decimal_places)

                    for rep in range(num_replicates):
                        # 生成该重复中的 △CT 值
                        delta_ct = round(random.gauss(delta_ct_mean, delta_ct_std), decimal_places)

                        # 生成该重复中的内参基因 CT 值（添加 ±0.05 的混淆值）
                        ref_ct_mean = ref_mean
                        ref_ct_values = generate_ct_values(ref_ct_mean, ref_std, 3)

                        # 计算该重复中目的基因的 CT 值
                        target_ct_mean_rep = ref_ct_mean + delta_ct
                        target_ct_values = generate_ct_values(target_ct_mean_rep, target_ct_std, 3)

                        # 计算目的基因和内参基因的 CT 平均值和标准差
                        target_ct_mean, target_ct_std = calculate_statistics(target_ct_values)
                        ref_ct_mean, ref_ct_std = calculate_statistics(ref_ct_values)

                        # 添加一行数据
                        row = [
                            sample,  # 样本名
                            treatment,  # 处理方式
                            f"rep {rep + 1}",  # 重复实验编号
                            *target_ct_values,  # 目的基因 CT 值（3 个样本重复）
                            target_ct_mean,  # 目的基因 CT 平均值
                            target_ct_std,  # 目的基因 CT 标准差
                            *ref_ct_values,  # 内参基因 CT 值（3 个样本重复）
                            ref_ct_mean,  # 内参基因 CT 平均值
                            ref_ct_std,  # 内参基因 CT 标准差
                            delta_ct,  # △CT 值
                            delta_ct_mean,  # 该处理方式的 △CT 值平均数
                            delta_ct_std,  # 该处理方式的 △CT 值标准差
                        ]
                        data.append(row)
                    config["used"]["money"] = str(float(config["used"]["money"]) + 3 * 3 * 2 * num_replicates)
            with open('config/config.ini', 'w') as configfile:
                config.write(configfile)

            # 创建 DataFrame
            df = pd.DataFrame(data, columns=[
                "Sample Name", "Group", "Repeat Number",
                f"{target_gene} CT   1", f"{target_gene} CT   2", f"{target_gene} CT   3",
                f"{target_gene} CT Mean", f"{target_gene} SD",
                f"{ref_gene} CT   1", f"{ref_gene} CT   2", f"{ref_gene} CT   3", f"{ref_gene} CT Mean",
                f"{ref_gene} CT SD",
                "△CT", "△CT Mean", "△CT SD"
            ])

            # 保存为 Excel 文件
            df.to_excel(output_file, index=False)
            print(f"Excel 文件已生成: {output_file}")

        # 用户输入
        sample_names = input("请输入样本名（用逗号分隔）: ").strip().split(",")
        if sample_names[0].lower() == "quit":
            load_main_from_exe()
        treatments = input("请输入处理方式（用逗号分隔）: ").strip().split(",")
        if treatments[0].lower() == "quit":
            load_main_from_exe()
        target_gene = input("请输入目的基因名称: ")
        if target_gene.lower() == "quit":
            load_main_from_exe()
        ref_gene = input("请输入内参基因名称: ")
        if ref_gene.lower() == "quit":
            load_main_from_exe()
        base_filename = input("请输入文件名（无需扩展名，例如 output）: ")
        if base_filename.lower() == "quit":
            load_main_from_exe()

        # 获取当前日期并格式化为 YYYYMMDD
        current_date = datetime.now().strftime("%Y%m%d")
        # 生成带日期的文件名
        output_file = f"{current_date}_{base_filename}.xlsx"

        # 为每个样品和处理方式的组合输入重复实验数、△CT 值平均数及标准差、内参基因 CT 值平均数及标准差
        replicates_info = {}
        for sample in sample_names:
            for treatment in treatments:
                num_replicates = input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的重复实验数: ")
                if num_replicates.lower() == "quit":
                    load_main_from_exe()
                else:
                    num_replicates = int(num_replicates)
                delta_ct_mean = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的 △CT 值平均数: ")
                delta_ct_std = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的 △CT 值标准差: ")
                ref_mean = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的内参基因 CT 值平均数: ")
                ref_std = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的内参基因 CT 值标准差: ")
                target_ct_std = get_input(f"请输入样本 '{sample}' 和处理方式 '{treatment}' 的目的基因 CT 值标准差: ")
                replicates_info[(sample, treatment)] = (
                    num_replicates, delta_ct_mean, delta_ct_std, ref_mean, ref_std, target_ct_std)

        # 创建 Excel 文件
        create_excel(sample_names, treatments, replicates_info, target_gene, ref_gene, output_file)

        input("回车后退回程序主界面")
        load_main_from_exe()
