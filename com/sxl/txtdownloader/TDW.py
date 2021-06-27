import base64
import os
import threading
from tkinter import *
from tkinter import simpledialog, filedialog
from tkinter.scrolledtext import ScrolledText

from com.sxl.txtdownloader import WebUtils, ConfUtils
from com.sxl.txtdownloader.ConfUtils import cf
from com.sxl.txtdownloader.icon import img

LOG_LINE_NUM = 0


class MyGUI:
    def __init__(self, init_window_name):
        # 测试模块
        self.init_window_name = init_window_name
        self.test_path_label = Label(self.init_window_name, text="测试路径：")
        self.test_path_Text = Text(self.init_window_name, width=40, height=1)  # 测试路径录入框
        self.test_encoding_label = Label(self.init_window_name, text="测试编码：")
        self.test_encoding_Text = Text(self.init_window_name, width=40, height=1)  # 测试编码录入框
        self.test_selector_label = Label(self.init_window_name, text="测试页面选择器：")
        self.test_selector_Text = Text(self.init_window_name, width=40, height=1)  # 测试页面选择器录入框
        self.test_content_button = Button(self.init_window_name, text="测试", bg="lightblue", width=10, height=1,
                                          command=self.test_web_content)

        # 输入模块
        self.list_path_label = Label(self.init_window_name, text="小说列表页面路径：")
        self.list_path_Text = Text(self.init_window_name, width=40, height=1)  # 小说列表路径录入框
        self.list_encoding_label = Label(self.init_window_name, text="小说列表页面编码(可选）：")
        self.list_encoding_Text = Text(self.init_window_name, width=40, height=1)  # 小说列表编码录入框
        self.list_selector_label = Label(self.init_window_name, text="列表页面选择器")
        self.list_selector_Text = Text(self.init_window_name, width=40, height=1)  # 列表页面选择器录入框

        self.chapter_url_prefix_label = Label(self.init_window_name, text="章节url前缀(可选)：")
        self.chapter_url_prefix_Text = Text(self.init_window_name, width=40, height=1)  # 章节url前缀录入框
        self.chapter_url_extract_button = Button(self.init_window_name, text="提取链接", bg="lightblue", width=10, height=1,
                                                 command=self.extract_chapter_url)
        self.chapter_encoding_label = Label(self.init_window_name, text="章节页面编码(可选）：")
        self.chapter_encoding_Text = Text(self.init_window_name, width=40, height=1)  # 章节页面编码录入框
        self.chapter_selector_label = Label(self.init_window_name, text="章节页面选择器")
        self.chapter_selector_Text = Text(self.init_window_name, width=40, height=1)  # 章节页面选择器录入框

        self.dst_path_label = Label(self.init_window_name, text="下载路径：")
        self.dst_path_Text = Text(self.init_window_name, width=40, height=1)  # 下载路径录入框
        self.dst_path_Button = Button(self.init_window_name, text="默认路径", bg="lightblue", width=10, height=1,
                                      command=self.get_current_path)

        self.txt_name_label = Label(self.init_window_name, text="下载文件/文件夹名：")
        self.txt_name_Text = Text(self.init_window_name, width=40, height=1)  # 下载txt文件名录入框

        self.merge_choice_v = StringVar()
        self.merge_choice_v.set('ON')
        self.merge_choice_label = Label(self.init_window_name, text="是否合并文件")
        self.merge_choice = Checkbutton(self.init_window_name, variable=self.merge_choice_v, text='合并文件',
                                        onvalue='ON', offvalue='OFF', command=self.merge_click_event)
        self.import_conf_button = Button(self.init_window_name, text="导入配置", bg="lightblue", width=10, height=1,
                                         command=self.import_conf)
        self.export_conf_button = Button(self.init_window_name, text="导出配置", bg="lightblue", width=10, height=1,
                                         command=self.export_conf)
        self.start_download_button = Button(self.init_window_name, text="开始下载", bg="lightblue", width=10, height=1,
                                            command=self.start_download)

        self.result_data_label = Label(self.init_window_name, text="处理结果展示：")
        self.result_data_Text = ScrolledText(self.init_window_name, width=105, height=50)

        # 参数
        self.txt_url_dict = {}

    # 设置窗口
    def set_window(self):
        self.init_window_name.title("网站小说下载工具_v1.0")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')   #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        # self.init_window_name.geometry('1068x681+10+10')
        self.init_window_name.geometry('1300x700+10+10')
        # self.init_window_name["bg"] = "pink"              #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)    #虚化，值越小虚化程度越高

        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(img))
        tmp.close()
        self.init_window_name.iconbitmap("tmp.ico")
        os.remove("tmp.ico")

        # 标签
        self.test_path_label.grid(row=0, column=0)
        self.test_encoding_label.grid(row=1, column=0)
        self.test_selector_label.grid(row=2, column=0)

        self.list_path_label.grid(row=4, column=0)
        self.list_encoding_label.grid(row=5, column=0)
        self.list_selector_label.grid(row=6, column=0)

        self.chapter_url_prefix_label.grid(row=7, column=0)
        self.chapter_encoding_label.grid(row=8, column=0)
        self.chapter_selector_label.grid(row=9, column=0)

        self.dst_path_label.grid(row=10, column=0)
        self.txt_name_label.grid(row=11, column=0)
        self.merge_choice_label.grid(row=12, column=0)

        self.result_data_label.grid(row=0, column=4)

        # 文本框
        self.test_path_Text.grid(row=0, column=1)
        self.test_encoding_Text.grid(row=1, column=1)
        self.test_selector_Text.grid(row=2, column=1)

        self.list_path_Text.grid(row=4, column=1)
        self.list_encoding_Text.grid(row=5, column=1)
        self.list_selector_Text.grid(row=6, column=1)

        self.chapter_url_prefix_Text.grid(row=7, column=1)
        self.chapter_encoding_Text.grid(row=8, column=1)
        self.chapter_selector_Text.grid(row=9, column=1)

        self.dst_path_Text.grid(row=10, column=1)
        self.txt_name_Text.grid(row=11, column=1)

        self.result_data_Text.grid(row=1, column=4, rowspan=15, columnspan=12)

        # 复选框
        self.merge_choice.grid(row=12, column=1)

        # 按钮
        self.test_content_button.grid(row=3, column=0, columnspan=3)
        self.chapter_url_extract_button.grid(row=6, column=3)
        self.dst_path_Button.grid(row=10, column=3)

        self.import_conf_button.grid(row=13, column=0)
        self.start_download_button.grid(row=13, column=1)
        self.export_conf_button.grid(row=13, column=2, columnspan=2)

    # 是否合并点击事件
    def merge_click_event(self):
        self.clear_result()
        self.print_result(self.merge_choice_v.get())

    # 测试页面内容
    def test_web_content(self):
        test_url = self.test_path_Text.get('0.0', 'end').strip()
        test_encoding = self.test_encoding_Text.get('0.0', 'end').strip()
        test_selector = self.test_selector_Text.get('0.0', 'end')
        if test_url is None:
            content = 'url为空！！！！！！'
        else:
            content = WebUtils.get_test_web_contents(test_url, test_encoding, test_selector)
        # content = str(len(content))
        self.clear_result()
        self.print_result(content)

    # 提取链接点击事件
    def extract_chapter_url(self):
        timer = threading.Thread(target=self.extract_chapter_url_timer)
        timer.daemon = True
        timer.start()
        return

    #  提取下载链接线程
    def extract_chapter_url_timer(self):
        self.clear_result()
        list_path = self.list_path_Text.get('0.0', 'end').strip()
        self.print_result('列表页面路径:' + list_path)
        if list_path == '':
            return
        list_encoding = self.list_encoding_Text.get('0.0', 'end').strip()
        self.print_result('列表页面编码:' + list_encoding)
        list_selector = self.list_selector_Text.get('0.0', 'end')
        self.print_result('列表选择器:' + list_selector)
        chapter_url_prefix = self.chapter_url_prefix_Text.get('0.0', 'end').strip()
        self.print_result('章节url前缀:' + chapter_url_prefix)
        self.txt_url_dict = WebUtils.get_chapter_list(list_path, list_encoding, list_selector, chapter_url_prefix)
        for title, url in self.txt_url_dict.items():
            msg = title + '\n' + url
            print(msg)
            self.print_result(msg)

    # 自动填充默认下载路径
    def get_current_path(self):
        self.dst_path_Text.delete('1.0', 'end')
        self.dst_path_Text.insert('insert', ConfUtils.get_current_path() + '\\download\\')
        return

    # 开始下载点击事件
    def start_download(self):
        timer = threading.Thread(target=self.start_download_timer)
        timer.daemon = True
        timer.start()
        return

    # 开始下载线程
    def start_download_timer(self):
        chapter_encoding = self.chapter_encoding_Text.get('0.0', 'end').strip()
        chapter_selector = self.chapter_selector_Text.get('0.0', 'end')
        self.extract_chapter_url_timer()
        is_merge = self.merge_choice_v.get()
        dst_path = self.dst_path_Text.get('0.0', 'end').strip()
        if dst_path == '':
            dst_path = ConfUtils.get_current_path() + '\\download'
        txt_name = dst_path + self.txt_name_Text.get('0.0', 'end').strip()
        for title, url in self.txt_url_dict.items():
            msg = '开始下载：' + title + '\n' + url
            print(msg)
            self.print_result(msg)
            content = WebUtils.get_txt_content(url, chapter_encoding, chapter_selector)
            if len(content.encode()) < 2000:
                self.print_result('长度过短，跳过下载')
                continue
            if is_merge == 'OFF':
                txt_name = dst_path + '\\' + title + '.txt'
            WebUtils.write_to_txt(txt_name, title, content)
        self.print_result('下载完成！！！！！！\n下载路径：' + dst_path)

    # 清空输出
    def clear_result(self):
        self.result_data_Text.delete('1.0', 'end')

    # 输出
    def print_result(self, result):
        self.result_data_Text.insert('insert', result + '\n')
        self.result_data_Text.see(END)

    # 导入配置
    def import_conf(self):
        # file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser('H:/')))
        file_path = filedialog.askopenfilename(title=u'选择文件')
        print('打开文件：', file_path)
        self.print_result('导入配置:' + file_path)
        cf.read(file_path, encoding='utf-8')
        self.list_path_Text.delete('1.0', 'end')
        self.list_path_Text.insert('insert', cf.get('my_conf', 'list_path'))
        self.list_encoding_Text.delete('1.0', 'end')
        self.list_encoding_Text.insert('insert', cf.get('my_conf', 'list_encoding'))
        self.list_selector_Text.delete('1.0', 'end')
        self.list_selector_Text.insert('insert', cf.get('my_conf', 'list_selector'))
        self.chapter_url_prefix_Text.delete('1.0', 'end')
        self.chapter_url_prefix_Text.insert('insert', cf.get('my_conf', 'chapter_url_prefix'))
        self.chapter_encoding_Text.delete('1.0', 'end')
        self.chapter_encoding_Text.insert('insert', cf.get('my_conf', 'chapter_encoding'))
        self.chapter_selector_Text.delete('1.0', 'end')
        self.chapter_selector_Text.insert('insert', cf.get('my_conf', 'chapter_selector'))
        self.merge_choice_v.set(cf.get('my_conf', 'is_merge'))
        self.dst_path_Text.delete('1.0', 'end')
        self.dst_path_Text.insert('insert', cf.get('my_conf', 'dst_path'))
        self.txt_name_Text.delete('1.0', 'end')
        self.txt_name_Text.insert('insert', cf.get('my_conf', 'txt_name'))

    # 导出配置
    def export_conf(self):
        conf_name = simpledialog.askstring(title='设置', prompt='请输入配置名：', initialvalue='my_conf')
        list_path = self.list_path_Text.get('0.0', 'end').strip()
        list_encoding = self.list_encoding_Text.get('0.0', 'end').strip()
        list_selector = self.list_selector_Text.get('0.0', 'end')
        chapter_url_prefix = self.chapter_url_prefix_Text.get('0.0', 'end').strip()
        chapter_encoding = self.chapter_encoding_Text.get('0.0', 'end').strip()
        chapter_selector = self.chapter_selector_Text.get('0.0', 'end')
        is_merge = self.merge_choice_v.get()
        dst_path = self.dst_path_Text.get('0.0', 'end').strip()
        txt_name = self.txt_name_Text.get('0.0', 'end').strip()
        conf_path = ConfUtils.get_current_path() + '/conf/' + conf_name + '.conf'
        ConfUtils.export(conf_path, list_path, list_encoding, list_selector, chapter_url_prefix, chapter_encoding,
                         chapter_selector,
                         is_merge, dst_path, txt_name)
        self.print_result('导出配置:' + os.path.abspath(conf_path))


def gui_start():
    window = Tk()  # 实例化出一个父窗口
    tdw_window = MyGUI(window)
    # 设置根窗口默认属性
    tdw_window.set_window()

    window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()
