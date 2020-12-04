from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Map
from pyecharts.charts import Page
from pyecharts.charts import Pie
from pyecharts.globals import ThemeType

from cache import mongodb

# 可视化 图标

# 定义 基本的计算机语言
computer_language = [
    'Java', 'C++', 'PHP', 'C', 'C#', '.NET', 'Python', 'Delphi', 'VB',
    'Perl', 'Ruby', 'js', 'Go', 'Erlang',
]

# 定义基本的深圳区
area = [
    "宝安", "龙华", "福田", "龙岗", "罗湖", "盐田", "坪山", "南山"
]

# 基本学历
education = [
    "不限", "初中", "高中", "大专", "高中", "本科", "硕士",  "博士",
]


#  用于计算语言占比 饼状图
def get_language_proportion():
    data = []
    for i in computer_language:
        # 匹配标题 含有这些语言的
        where = {
            '$or': [
                {'job_name': {'$regex': ".*" + i + ".*", '$options': 'i'}},
                {'tags': {'$regex': ".*" + i + ".*", '$options': 'i'}},
                {'search_name': {'$regex': ".*" + i + ".*", '$options': 'i'}}
            ]
        }
        count = mongodb.get_count_by_where(where)
        tmp = (i, count)
        data.append(tmp)
    c = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT)).add(
            "语言占比图",
            data
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="语言占比图", ),
            legend_opts=opts.LegendOpts(pos_left="20%"))
    )
    return c


def get_all_chart():
    page = Page()
    page.add(get_language_proportion())
    page.add(get_salary_proportion())
    page.add(get_map())
    #
    page.add(get_education_background())
    page.render("temp/all.html")
    # get_education_background()

    pass


# 薪资柱状图
def get_salary_proportion():
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="平均薪资柱状图", ),
        legend_opts=opts.LegendOpts(pos_left="20%")
    )
    for i in computer_language:
        # 匹配标题 含有这些语言的
        where = {
            '$or': [
                {'job_name': {'$regex': ".*" + i + ".*", '$options': 'i'}},
                {'tags': {'$regex': ".*" + i + ".*", '$options': 'i'}},
                {'search_name': {'$regex': ".*" + i + ".*", '$options': 'i'}}
            ]
        }
        count_salary = 0
        query_res = mongodb.get_info_by_where(where)
        line = 0
        for v in query_res:
            line = line + 1
            salary = v["salary"]
            res = salary.split("-")
            count_salary = count_salary + (int(res[0]) * 1000)

        average_salary = count_salary // line
        bar.add_yaxis(i, [average_salary], bar_width=30)
    bar.add_xaxis([])

    return (
        bar
    )


# 地区分布占比
def get_map():
    maps = Map(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    value = []
    for i in area:
        where = {
            'job_area': {'$regex': ".*" + i + ".*"},
        }
        count = mongodb.get_count_by_where(where)
        value.append((i + "区", count))
    maps.add("区域", value, "深圳")
    maps.set_global_opts(
        title_opts=opts.TitleOpts(title="岗位地区需求图", ),
        legend_opts=opts.LegendOpts(pos_left="20%"))
    return (
        maps
    )


# 学历对应招聘数量
def get_education_background():
    bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="学历占比", ),
        legend_opts=opts.LegendOpts(pos_left="20%")
    )
    bar.add_xaxis(education)
    value = []
    for i in education:
        where = {
            'experience': {'$regex': ".*" + i + ".*"},
        }
        count = mongodb.get_count_by_where(where)
        value.append(count)

    bar.add_yaxis("要求学历招聘", value, bar_width=20)
    bar.set_colors("blue")
    return (
        bar
    )


