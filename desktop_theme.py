"""Native desktop styles and scope summaries."""
import colorsys
import ntpath

BG = '#f3f6fb'
INK = '#172a46'
MUTED = '#64758b'
NAVY = '#14243e'


def apply_theme(style):
    style.theme_use('clam')
    style.configure('.', font=('Microsoft YaHei', 10), background=BG, foreground=INK)
    style.configure('TFrame', background=BG)
    style.configure('Card.TFrame', background='white')
    style.configure('TLabel', background=BG, foreground=INK)
    style.configure('Muted.TLabel', foreground=MUTED)
    style.configure('Card.TLabel', background='white', foreground=MUTED)
    style.configure('Metric.TLabel', background='white', foreground=INK, font=('Microsoft YaHei', 21, 'bold'))
    style.configure('Scope.TLabel', background='#fff4dd', foreground='#85551c', padding=10)
    style.configure('TButton', background='white', foreground=INK, borderwidth=0, padding=(14, 9))
    style.map('TButton', background=[('active', '#e4ecf8')], foreground=[('disabled', '#a1adbc')])
    style.configure('Primary.TButton', background='#2563eb', foreground='white')
    style.map('Primary.TButton', background=[('active', '#1d4ed8'), ('disabled', '#a8bce6')], foreground=[('disabled', '#f3f6fb')])
    style.configure('Danger.TButton', background='#fff0ed', foreground='#a94c3f')
    style.configure('Treeview', rowheight=38, font=('Microsoft YaHei', 10), background='white', fieldbackground='white', foreground=INK, borderwidth=0)
    style.map('Treeview', background=[('selected', '#dbeafe')], foreground=[('selected', '#183662')])
    style.configure('Treeview.Heading', background='#edf2f9', foreground=MUTED, relief='flat', padding=(8, 10), font=('Microsoft YaHei', 9, 'bold'))
    style.configure('TNotebook', background=BG, borderwidth=0)
    style.configure('TNotebook.Tab', padding=(20, 10), background='#e8edf6', foreground=MUTED)
    style.map('TNotebook.Tab', background=[('selected', 'white')], foreground=[('selected', '#2563eb')])
    style.configure('Horizontal.TProgressbar', background='#2563eb', troughcolor='#e4ebf6', borderwidth=0)
    style.configure('TEntry', fieldbackground='white', padding=7)
    style.configure('TCombobox', fieldbackground='white', padding=6)


def scope_message(root):
    drive, tail = ntpath.splitdrive(root)
    if drive and tail in {'/', '\\'}:
        return f'整盘扫描范围：{root}。权限、链接跳过等原因仍可能使统计不完整。'
    return f'仅扫描文件夹：{root}。不包含同盘其他目录，不能代表整个盘的占用。'


def drive_colors(path):
    drive = ntpath.splitdrive(path)[0].upper()
    seed = sum(ord(c) for c in drive) if drive else 1
    hue = (seed * 0.61803398875) % 1
    return ['#' + ''.join(f'{round(v * 255):02x}' for v in colorsys.hsv_to_rgb((hue + i * .081) % 1, .65, .76)) for i in range(12)]
