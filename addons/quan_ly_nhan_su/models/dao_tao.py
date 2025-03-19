# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DaoTao(models.Model):
    _name = "dao_tao"
    _description = "Quá trình đào tạo của nhân viên"
    _rec_name = "ten_khoa_hoc"
    
    # Thông tin cơ bản
    ten_khoa_hoc = fields.Char(string="Tên khóa học/đào tạo", required=True)
    
    # Mối quan hệ
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    
    # Thông tin đào tạo
    loai_dao_tao = fields.Selection([
        ('noi_bo', 'Đào tạo nội bộ'),
        ('ben_ngoai', 'Đào tạo bên ngoài'),
        ('tu_hoc', 'Tự học')
    ], string="Loại đào tạo", required=True)
    don_vi_dao_tao = fields.Char(string="Đơn vị đào tạo")
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc")
    so_gio = fields.Float(string="Số giờ đào tạo")
    chi_phi = fields.Float(string="Chi phí")
    
    # Kết quả đào tạo
    ket_qua = fields.Selection([
        ('dat', 'Đạt'),
        ('khong_dat', 'Không đạt'),
        ('dang_hoc', 'Đang học')
    ], string="Kết quả", default='dang_hoc')
    chung_chi = fields.Char(string="Chứng chỉ đạt được")
    hinh_anh_chung_chi = fields.Binary(string="Hình ảnh chứng chỉ")
    file_name = fields.Char(string="Tên file")
    
    # Ghi chú
    ghi_chu = fields.Text(string="Ghi chú")
    
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError(_("Ngày bắt đầu không thể sau ngày kết thúc!"))
