# -*- coding: utf-8 -*-
{
    'name': "quan_ly_cong_viec",

    'summary': """
        Module quản lý dự án và công việc tích hợp với nhân sự""",

    'description': """
        Mô đun quản lý công việc cho doanh nghiệp:
        - Quản lý dự án
        - Phân công công việc
        - Theo dõi tiến độ
        - Phân bổ nguồn lực
        - Báo cáo hiệu suất
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Project Management',
    'version': '0.1',

    # Quan trọng: Phải phụ thuộc vào module quan_ly_nhan_su
    'depends': ['base', 'quan_ly_nhan_su'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/du_an.xml',
        'views/cong_viec.xml',
        'views/nguoi_tham_gia.xml',
        'views/bao_cao_tien_do.xml',
        'views/phan_bo_nguon_luc.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
