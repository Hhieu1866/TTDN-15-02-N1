# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PhanBoNguonLuc(models.Model):
    _name = "phan_bo_nguon_luc"
    _description = "Phân bổ nguồn lực"
    _rec_name = "ten_nguon_luc"
    
    ten_nguon_luc = fields.Char(string="Tên nguồn lực", required=True)
    
    # Phân loại
    loai_nguon_luc = fields.Selection([
        ('nhan_luc', 'Nhân lực'),
        ('tai_chinh', 'Tài chính'),
        ('vat_tu', 'Vật tư'),
        ('thiet_bi', 'Thiết bị'),
        ('khac', 'Khác')
    ], string="Loại nguồn lực", required=True)
    
    # Mối quan hệ - chỉ được gán cho dự án HOẶC công việc cụ thể
    du_an_id = fields.Many2one('du_an', string="Dự án")
    cong_viec_id = fields.Many2one('cong_viec', string="Công việc", domain="[('du_an_id', '=', du_an_id)]")
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên")
    
    # Thông tin phân bổ
    mo_ta = fields.Text(string="Mô tả")
    so_luong = fields.Float(string="Số lượng", default=1.0)
    don_vi = fields.Char(string="Đơn vị")
    don_gia = fields.Float(string="Đơn giá")
    chi_phi = fields.Float(string="Chi phí", compute="_compute_chi_phi", store=True)
    
    # Thời gian
    ngay_phan_bo = fields.Date(string="Ngày phân bổ", required=True, default=fields.Date.today)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu sử dụng")
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc sử dụng")
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('du_kien', 'Dự kiến'),
        ('da_phan_bo', 'Đã phân bổ'),
        ('dang_su_dung', 'Đang sử dụng'),
        ('da_hoan_tra', 'Đã hoàn trả')
    ], string="Trạng thái", default='du_kien')
    
    @api.depends('so_luong', 'don_gia')
    def _compute_chi_phi(self):
        for record in self:
            record.chi_phi = record.so_luong * record.don_gia
    
    @api.constrains('du_an_id', 'cong_viec_id')
    def _check_project_or_task(self):
        for record in self:
            if not record.du_an_id and not record.cong_viec_id:
                raise ValidationError(_("Phải chọn ít nhất một dự án hoặc công việc!"))
            if record.cong_viec_id and record.du_an_id and record.cong_viec_id.du_an_id != record.du_an_id:
                raise ValidationError(_("Công việc phải thuộc dự án đã chọn!"))
    
    @api.onchange('cong_viec_id')
    def _onchange_cong_viec(self):
        if self.cong_viec_id and not self.du_an_id:
            self.du_an_id = self.cong_viec_id.du_an_id
