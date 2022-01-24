import re
import os
import json
from matplotlib import pyplot as plt
from matplotlib import rcParams

#汉字可能会出现乱码，这里事先确定好字体
rcParams['font.family'] = 'SimHei'
#figsize参数决定画布的大小
fig, ax = plt.subplots(figsize=(12,8))  # 创建图实例

def get_data(flag):
    works = {}
    dir_list = os.listdir("./data/2022-01-14")
    for json_data in dir_list:
        with open("./data/2022-01-14/"+json_data,'r',encoding="utf-8") as f:
            content = f.read()
        dict_data = json.loads(content)
        #key中是时间
        key, = dict_data.keys()
        #value中是作品的详细信息
        value, = dict_data.values()
        if flag == "work":
            for work in value:
                if work["title"] in works.keys():
                    pass
                else:
                    works.update({work["title"]:[[],[]]})
                works[work["title"]][1].append(work["status"]["view"])
                #截取小时和分钟的数据作为横坐标
                works[work["title"]][0].append(key[-8:-3])
        elif flag == "time":
            works.update({key:[]})
            for work in value:
                works[key].append([work["title"],work["status"]["view"]])
    print(works)
    return works

#格式化纵轴的坐标值
def currency(x,pos):
    if x >= 1e6:
        s = '{:1.3f}M'.format(x*1e-6)
    else:
        s = '{:1.0f}K'.format(x*1e-3)
    return s

#绘制同一作品不同时间段的图像
def one_work(title,x,y):
    plt.cla()
    ax.set_xlabel("时间",fontproperties="SimHei",fontsize=20)
    x_labels = ax.get_xticklabels()
    ax.set_ylabel("观看人数",fontproperties="SimHei",fontsize=20)
    #rotation参数设置旋转角度，horizontalalignment设置水平对齐
    plt.setp(x_labels, rotation=45, horizontalalignment='right')
    ax.yaxis.set_major_formatter(currency)
    #title是作品名称，x是时间，y是观看人数
    ax.plot(x,y,label=title)
    ax.legend()
    try:
        #保存绘制的图形到磁盘，transparent参数决定是否支持透明，dpi参数决定分辨率
        fig.savefig('./pic/work/{key}.png'.format(key=title), transparent=False, dpi=80, bbox_inches="tight")
    except FileNotFoundError:
        title = re.sub("[/ \\\ : * \" < > | ? ？]","",title)
        fig.savefig('./pic/work/{key}.png'.format(key=title), transparent=False, dpi=80, bbox_inches="tight")
    except:
        pass

# #绘制不同作品同一时间的图像
# def one_time(x,y,title):
#     plt.cla()
#     ax.set_xlabel("作品名称",fontproperties="SimHei",fontsize=20)
#     x_labels = ax.get_xticklabels()
#     ax.set_ylabel("观看人数",fontproperties="SimHei",fontsize=20)
#     #rotation参数设置旋转角度，horizontalalignment设置水平对齐
#     plt.setp(x_labels, rotation=45, horizontalalignment='right')
#     ax.yaxis.set_major_formatter(currency)
#     #title是作品名称，x是时间，y是观看人数
#     ax.plot(x,y,label=title)
#     ax.legend()
#     try:
#         #保存绘制的图形到磁盘，transparent参数决定是否支持透明，dpi参数决定分辨率
#         fig.savefig('./pic/time/{key}.png'.format(key=title), transparent=False, dpi=80, bbox_inches="tight")
#     except FileNotFoundError:
#         #文件名错误可能是因为文件名命名错误
#         title = re.sub("[/ \\\ : * \" < > | ? ？]","",title)
#         fig.savefig('./pic/time/{key}.png'.format(key=title), transparent=False, dpi=80, bbox_inches="tight")

def main():
    if os.path.exists("./pic"):
        pass
    else:
        os.mkdir("./pic")
    if os.path.exists("./pic/work"):
        pass
    else:
        os.mkdir("./pic/work")
    if os.path.exists("./pic/time"):
        pass
    else:
        os.mkdir("./pic/time")

    works = get_data("work")
    for key,value in works.items():
        # one_work(key,(value[0]),(value[1]))
        try:
            one_work(key,value[0],value[1])
        except UserWarning:
            print("ERROR:",key)


if __name__ == "__main__":
    main()
