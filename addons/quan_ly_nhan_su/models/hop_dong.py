# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HopDong(models.Model):
    _name = "hop_dong"
    _description = "Quản lý hợp đồng lao động"
    _rec_name = "ma_hop_dong"

    ma_hop_dong = fields.Char(string="Mã hợp đồng", required=True, index=True)
    ten_hop_dong = fields.Char(string="Tên hợp đồng", required=True, tracking=True)
    
    # Các mối quan hệ
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, tracking=True)
    
    # Thông tin hợp đồng
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Hợp đồng thử việc'),
        ('xac_dinh_thoi_han', 'Hợp đồng xác định thời hạn'),
        ('khong_xac_dinh_thoi_han', 'Hợp đồng không xác định thời hạn'),
        ('thoi_vu', 'Hợp đồng thời vụ')
    ], string="Loại hợp đồng", required=True, tracking=True)
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True, tracking=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", tracking=True)
    luong_co_ban = fields.Float(string="Lương cơ bản", tracking=True)
    phu_cap = fields.Float(string="Phụ cấp", tracking=True)
    ngay_ky = fields.Date(string="Ngày ký hợp đồng", tracking=True)
    file_hop_dong = fields.Binary(string="File hợp đồng")
    file_name = fields.Char(string="Tên file")
    trang_thai = fields.Selection([
        ('draft', 'Dự thảo'),
        ('waiting', 'Chờ ký'),
        ('active', 'Đang hiệu lực'),
        ('expired', 'Hết hiệu lực'),
        ('terminated', 'Đã chấm dứt')
    ], string="Trạng thái", default='draft', tracking=True)
    
    # Ràng buộc Python
    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_dates(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_bat_dau > record.ngay_ket_thuc:
                raise ValidationError(_("Ngày bắt đầu không thể sau ngày kết thúc!"))
    
    @api.constrains('luong_co_ban')
    def _check_luong(self):
        for record in self:
            if record.luong_co_ban and record.luong_co_ban <= 0:
                raise ValidationError(_("Lương cơ bản phải lớn hơn 0!"))
    
    
    # Cập nhật trạng thái hợp đồng tự động
    @api.model
    def _cron_update_contract_status(self):
        today = fields.Date.today()
        # Cập nhật hợp đồng hết hạn
        expired_contracts = self.search([
            ('ngay_ket_thuc', '<', today),
            ('trang_thai', '=', 'active')
        ])
        expired_contracts.write({'trang_thai': 'expired'})
        
        # Cập nhật hợp đồng mới có hiệu lực
        active_contracts = self.search([
            ('ngay_bat_dau', '<=', today),
            ('ngay_ket_thuc', '>=', today),
            ('trang_thai', '=', 'waiting')
        ])
        active_contracts.write({'trang_thai': 'active'})
