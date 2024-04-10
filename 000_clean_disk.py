import os
import copy
import argparse

def make_parser():
    parser = argparse.ArgumentParser("tools")
    # --src_dir：从哪里开始搜索，比如你要清理C盘可以写C://，你要清理D盘可以写D://
    parser.add_argument("--src_dir", default='', type=str, help="src_dir")
    # --delete：是否执行真正的删除。如果不加这个参数，只会降序打印文件路径和文件大小
    parser.add_argument('--delete', action='store_true', help='delete files?')
    # 查找的文件后缀。多个的话用空格隔开。不填的话表示任何后缀都查找。
    parser.add_argument('--exts', type=str, nargs="+", default=[], help='file extensions, like \'.mp4\' \'.jpg\'')
    # 只打印文件最大的topk个
    parser.add_argument("--print_topk", default=100, type=int, help="print_topk")
    return parser


def search_files(root, exts, file_paths, file_sizes):
    try:
        path_dir = os.listdir(root)
    except Exception as e:
        # PermissionError: [WinError 5] 拒绝访问。
        print(e)
        return file_paths, file_sizes
    for name in path_dir:
        path = os.path.join(root, name)
        if os.path.isfile(path):
            if len(exts) == 0:
                file_paths.append(path)
                file_sizes.append(os.path.getsize(path))
            else:
                ext = os.path.splitext(path)[1]
                if ext in exts:
                    file_paths.append(path)
                    file_sizes.append(os.path.getsize(path))
        elif os.path.isdir(path):
            file_paths, file_sizes = search_files(path, exts, file_paths, file_sizes)
    return file_paths, file_sizes


def clean_disk(args):
    file_paths = []   # 文件路径
    file_sizes = []   # 文件大小
    # 递归获取 文件路径、文件大小
    file_paths, file_sizes = search_files(copy.deepcopy(args.src_dir), args.exts, file_paths, file_sizes)
    print('=========================== search files Done. ===========================')

    # 冒泡排序文件大小
    # bubble sort
    n = len(file_paths)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if file_sizes[j] < file_sizes[j + 1]:
                temp = file_sizes[j]
                file_sizes[j] = file_sizes[j + 1]
                file_sizes[j + 1] = temp
                temp = file_paths[j]
                file_paths[j] = file_paths[j + 1]
                file_paths[j + 1] = temp

    # 打印文件路径、文件大小。
    print('n=%d' % (n, ))
    for i, file_path in enumerate(file_paths):
        if i < args.print_topk:
            print('%s %dB'%(file_path, file_sizes[i]))
        if args.delete:
            os.remove(file_path)


'''
这是咩咩写的清理电脑磁盘的工具。示例：

清理D盘的压缩包（不删，仅打印文件路径、文件大小）:
python 000_clean_disk.py --src_dir D:// --exts .zip .rar .bz2

清理D盘的压缩包（真的删除，加上--delete）:
python 000_clean_disk.py --src_dir D:// --delete --exts .zip .rar .bz2

清理C盘的视频（不删，仅打印）:
python 000_clean_disk.py --src_dir C:// --exts .mp4 .flv .avi

清理C盘的图片（不删，仅打印）:
python 000_clean_disk.py --src_dir C:// --exts .jpg .jpeg .png .JPG .JPEG .PNG



'''
if __name__ == "__main__":
    args = make_parser().parse_args()
    clean_disk(args)









